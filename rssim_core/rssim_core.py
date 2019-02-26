"""
Implements RSSim class - base class for game launch and main loop.
"""
from ctypes import c_long, windll
from sqlite3 import connect
from time import perf_counter
from os import path, mkdir
from shutil import copyfile
from logging import FileHandler, Formatter, getLogger
from datetime import datetime

from pyglet import gl, resource
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from pyshaders import from_files_names

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException
from rssim_core import *


class RSSim:
    """
    Makes game ready to play: creates app instance, checks for updates and implements main game loop.
    """
    def __init__(self):
        """
        Properties:
              user_db_connection      connection to the user DB (stores game state and user-defined settings)
              user_db_cursor          user DB cursor (is used to execute user DB queries)
              config_db_connection    connection to the config DB (stores all configuration
                                      that is not designed to be managed by user)
              config_db_cursor        configuration DB cursor (is used to execute configuration DB queries)
              logger                  main game logger
              log_level               log level for base game logger
              surface                 surface to draw all UI objects on
              batches                 batches to group all labels and sprites
              groups                  defines drawing layers (some labels and sprites behind others)
              main_frame_shader       shader for main frame primitive (responsible for button borders,
                                      UI screens background, main app border)
              app                     App object, is responsible for high-level properties, UI and events
        """
        # determine if video adapter supports all game textures, if not - raise specific exception
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < REQUIRED_TEXTURE_SIZE:
            raise VideoAdapterNotSupportedException

        # determine if screen resolution meets requirements, if not - raise specific exception
        if windll.user32.GetSystemMetrics(0) < MIN_RESOLUTION_WIDTH \
                or windll.user32.GetSystemMetrics(1) < MIN_RESOLUTION_HEIGHT:
            raise MonitorNotSupportedException

        # determine if user launches app for the first time, if yes - create game save
        if not path.exists('db/user.db'):
            copyfile('db/default.db', 'db/user.db')

        # add resources: special font, images and textures
        resource.path = ['font', 'img', 'img/textures.zip']
        resource.reindex()
        # create database connections and cursors
        self.user_db_connection = connect('db/user.db')
        self.user_db_cursor = self.user_db_connection.cursor()
        self.config_db_connection = connect('db/config.db')
        self.config_db_cursor = self.config_db_connection.cursor()
        # check if game was updated from previous version (0.9.0 and higher are supported)
        self.on_check_for_updates()
        # set up the main logger; if logs are turned on, create log file
        self.user_db_cursor.execute('SELECT log_level FROM log_options')
        self.log_level = self.user_db_cursor.fetchone()[0]
        self.logger = getLogger('root')
        current_datetime = datetime.now()
        if self.log_level < LOG_LEVEL_OFF:
            if not path.exists('logs'):
                mkdir('logs')

            logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                       .format(str(current_datetime.date()), current_datetime.time().hour,
                                               current_datetime.time().minute, current_datetime.time().second,
                                               current_datetime.time().microsecond),
                                       encoding='utf8')
            logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(logs_handler)

        self.logger.setLevel(self.log_level)
        self.logger.info('START INIT')
        self.logger.debug('DB connection set up successfully')
        # set blending mode; this is required to correctly draw transparent textures
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.logger.debug('blending set successfully')
        # create batches and groups for text labels, sprites and textures
        self.batches = {}
        numbered_batches = []
        for i in range(5):
            numbered_batches.append(Batch())

        self.batches['main_batch'] = numbered_batches[0]
        self.logger.debug('main batch created successfully')
        self.batches['mini_map_batch'] = numbered_batches[2]
        self.logger.debug('mini map batch created successfully')
        self.batches['main_frame'] = numbered_batches[3]
        self.logger.debug('main frame batch created successfully')
        self.batches['ui_batch'] = numbered_batches[4]
        self.logger.debug('ui batch created successfully')
        self.groups = {}
        numbered_groups = []
        for i in range(12):
            numbered_groups.append(OrderedGroup(i))

        self.groups['environment'] = numbered_groups[0]
        self.logger.debug('environment group created successfully')
        self.groups['main_map'] = numbered_groups[1]
        self.logger.debug('main_map group created successfully')
        self.groups['signal'] = numbered_groups[2]
        self.logger.debug('signal group created successfully')
        self.groups['train'] = numbered_groups[2]
        self.logger.debug('train group created successfully')
        self.groups['boarding_light'] = numbered_groups[3]
        self.logger.debug('boarding_light group created successfully')
        self.groups['environment_2'] = numbered_groups[4]
        self.logger.debug('environment_2 group created successfully')
        self.groups['twilight'] = numbered_groups[5]
        self.logger.debug('twilight group created successfully')
        self.groups['mini_environment'] = numbered_groups[6]
        self.logger.debug('mini_environment group created successfully')
        self.groups['mini_map'] = numbered_groups[7]
        self.logger.debug('mini_map group created successfully')
        self.groups['mini_environment_2'] = numbered_groups[8]
        self.logger.debug('mini_environment_2 group created successfully')
        self.groups['main_frame'] = numbered_groups[9]
        self.logger.debug('main_frame group created successfully')
        self.groups['button_background'] = numbered_groups[10]
        self.logger.debug('button_background group created successfully')
        self.groups['exp_money_time'] = numbered_groups[10]
        self.logger.debug('exp_money_time group created successfully')
        self.groups['button_text'] = numbered_groups[11]
        self.logger.debug('button_text group created successfully')
        self.main_frame_shader = from_files_names('shaders/main_frame/shader.vert', 'shaders/main_frame/shader.frag')
        # create surface
        surface = Window(width=MIN_RESOLUTION_WIDTH, height=MIN_RESOLUTION_HEIGHT,
                         caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)
        self.logger.debug(f'surface {surface.width}x{surface.height} created successfully')
        self.surface = surface
        # flip the surface so user knows game has launched and is loading now
        self.surface.flip()
        # create App object
        self.app = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                              config_db_cursor=self.config_db_cursor,
                              surface=self.surface, batches=self.batches, groups=self.groups, loader=self)
        self.logger.debug('app created successfully')
        # activate app after it is created
        self.app.on_activate()
        self.logger.debug('app activated successfully')
        # initially app is created using default minimal screen resolution; now we change it to user resolution
        self.app.on_change_screen_resolution(self.app.settings.model.screen_resolution)
        self.logger.debug('screen resolution changed to {}'.format(self.app.settings.model.screen_resolution))
        # and same about fullscreen mode
        if self.app.settings.model.fullscreen_mode and self.app.model.fullscreen_mode_available:
            self.logger.debug('fullscreen mode is turned on')
            self.app.on_fullscreen_mode_turned_on()
            self.logger.debug('fullscreen mode was set successfully')
        else:
            self.logger.debug('fullscreen mode is turned off')

        self.logger.info('END INIT')

        @surface.event
        def on_draw():
            """
            Implements on_draw event handler for surface. Handler is attached using @surface.event decoration.
            This handler clears surface and calls draw() function for all batches (inserts shaders if required)
            """
            self.logger.info('START ON_DRAW')
            # clear surface
            self.surface.clear()
            self.logger.debug('surface cleared')
            # draw main batch: environment, main map, signals, trains
            self.batches['main_batch'].draw()
            self.logger.debug('main batch is drawn now')
            # draw mini map batch: mini map
            self.batches['mini_map_batch'].draw()
            self.logger.debug('mini map batch is drawn now')
            # draw main frame batch with main frame shader: main app borders, button borders, UI screens background
            self.main_frame_shader.use()
            self.app.on_set_up_main_frame_shader_uniforms(self.main_frame_shader)
            self.batches['main_frame'].draw()
            self.main_frame_shader.clear()
            self.logger.debug('main frame is drawn now')
            # draw ui batch: text labels, buttons
            self.batches['ui_batch'].draw()
            self.logger.debug('ui batch is drawn now')
            self.logger.info('END ON_DRAW')

        @surface.event
        def on_mouse_press(x, y, button, modifiers):
            """
            Implements on_mouse_press event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user presses any mouse button.
            This handler simply triggers all existing on_mouse_press handlers
            (from buttons, map move, or app window move).

            :param x:               mouse cursor X position inside the app window
            :param y:               mouse cursor Y position inside the app window
            :param button:          determines which mouse button was pressed
            :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
            """
            self.logger.info('START ON_MOUSE_PRESS')
            for h in self.app.on_mouse_press_handlers:
                self.logger.debug('moving to the next handler')
                h(x, y, button, modifiers)

            self.logger.info('END ON_MOUSE_PRESS')

        @surface.event
        def on_mouse_release(x, y, button, modifiers):
            """
            Implements on_mouse_release event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user releases any mouse button.
            This handler simply triggers all existing on_mouse_release handlers
            (from buttons, map move, or app window move).

            :param x:               mouse cursor X position inside the app window
            :param y:               mouse cursor Y position inside the app window
            :param button:          determines which mouse button was pressed
            :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
            """
            self.logger.info('START ON_MOUSE_RELEASE')
            for h in self.app.on_mouse_release_handlers:
                self.logger.debug('moving to the next handler')
                h(x, y, button, modifiers)

            self.logger.info('END SURFACE.ON_MOUSE_RELEASE')

        @surface.event
        def on_mouse_motion(x, y, dx, dy):
            """
            Implements on_mouse_motion event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user moves the mouse cursor.
            This handler simply triggers all existing on_mouse_motion handlers
            (from buttons, map move, or app window move).

            :param x:               mouse cursor X position inside the app window
            :param y:               mouse cursor Y position inside the app window
            :param dx:              relative X position from the previous mouse position
            :param dy:              relative Y position from the previous mouse position
            """
            self.logger.info('START SURFACE.ON_MOUSE_MOTION')
            for h in self.app.on_mouse_motion_handlers:
                self.logger.debug('moving to the next handler')
                h(x, y, dx, dy)

            self.logger.info('END ON_MOUSE_MOTION')

        @surface.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            """
            Implements on_mouse_drag event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user moves the mouse cursor with any mouse button being held down.
            This handler simply triggers all existing on_mouse_drag handlers (from map move or app window move).

            :param x:               mouse cursor X position inside the app window
            :param y:               mouse cursor Y position inside the app window
            :param dx:              relative X position from the previous mouse position
            :param dy:              relative Y position from the previous mouse position
            :param buttons:         determines which mouse button was pressed
            :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
            """
            self.logger.info('START ON_MOUSE_DRAG')
            for h in self.app.on_mouse_drag_handlers:
                self.logger.debug('moving to the next handler')
                h(x, y, dx, dy, buttons, modifiers)

            self.logger.info('END ON_MOUSE_DRAG')

        @surface.event
        def on_mouse_leave(x, y):
            """
            Implements on_mouse_leave event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user moves the mouse cursor and it leaves the app window.
            This handler simply triggers all existing on_mouse_leave handlers (from buttons).

            :param x:               mouse cursor X position
            :param y:               mouse cursor Y position
            """
            self.logger.info('START ON_MOUSE_LEAVE')
            for h in self.app.on_mouse_leave_handlers:
                self.logger.debug('moving to the next handler')
                h(x, y)

            self.logger.info('END ON_MOUSE_LEAVE')

    def run(self):
        """
        Implements main game loop.
        """
        self.logger.info('START GAME LOOP')
        # fps_timer is used to determine if it's time to recalculate FPS
        fps_timer = 0.0
        self.logger.debug(f'FPS timer: {fps_timer}')
        while True:
            time_1 = perf_counter()
            self.logger.debug('START FRAME')
            # dispatch_events() launches keyboard and mouse handlers implemented above
            self.surface.dispatch_events()
            self.logger.debug('all events dispatched')
            # increment in-game time
            self.app.game.on_update_time()
            self.logger.debug('time updated')
            # on_update_view() checks if all views content is up-to-date and opacity is correct
            self.app.on_update_view()
            self.logger.debug('all views updated')
            # call on_draw() handler implemented above
            self.surface.dispatch_event('on_draw')
            # flip the surface so user can see all the game content
            self.surface.flip()
            self.logger.debug('all stuff is drawn')
            self.logger.debug('END FRAME')
            time_4 = perf_counter()
            # FPS is recalculated every FPS_INTERVAL seconds
            if perf_counter() - fps_timer > FPS_INTERVAL:
                self.app.on_update_fps(round(float(1/(time_4 - time_1))))
                self.logger.info(f'FPS: {self.app.fps.model.fps}')
                fps_timer = perf_counter()
                self.logger.debug(f'FPS timer: {fps_timer}')

    def on_check_for_updates(self):
        """
        Checks user database version. If it is lower than current game version, it means user has just updated the app.
        All migration DB scripts need to be executed in chain, from earliest to latest, step by step.
        Results can be viewed in special ".update_log" file in logs directory.
        """
        # create logs directory if it does not exist
        if not path.exists('logs'):
            mkdir('logs')

        logger = getLogger('update_log')
        # create .update_log file
        current_datetime = datetime.now()
        logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.update_log'
                                   .format(str(current_datetime.date()), current_datetime.time().hour,
                                           current_datetime.time().minute, current_datetime.time().second,
                                           current_datetime.time().microsecond))
        logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(logs_handler)
        # for now log level is set to DEBUG, but can also be set to LOG_LEVEL_INFO
        logger.setLevel(LOG_LEVEL_DEBUG)
        logger.info('START CHECK_FOR_UPDATES')
        # If version does not exist, DB version is 0.9.0.
        # Just increment version here, no other DB changes.
        self.user_db_cursor.execute('SELECT * FROM sqlite_master WHERE type = "table" AND tbl_name = "version"')
        if len(self.user_db_cursor.fetchall()) == 0:
            logger.debug('version info not found')
            self.user_db_cursor.execute('CREATE TABLE version (major integer, minor integer, patch integer)')
            logger.debug('version table created')
            self.user_db_cursor.execute('INSERT INTO version VALUES (0, 9, 1)')
            logger.debug('version 0.9.1 set')
            self.user_db_connection.commit()

        # If version exists, read it from user DB.
        # If current game version is higher, use migration scripts one by one.
        # Migration script file is named "<version>.sql"
        self.user_db_cursor.execute('SELECT * FROM version')
        user_db_version = self.user_db_cursor.fetchone()
        logger.debug(f'user DB version: {user_db_version}')
        logger.debug(f'current game version: {CURRENT_VERSION}')
        if user_db_version < CURRENT_VERSION:
            logger.debug('upgrading database...')
            for patch in range(user_db_version[2] + 1, CURRENT_VERSION[2] + 1):
                logger.debug(f'start 0.9.{patch} migration')
                with open(f'db/patch/09{patch}.sql', 'r') as migration:
                    # simply execute each line in the migration script
                    for line in migration.readlines():
                        self.user_db_cursor.execute(line)
                        logger.debug(f'executed request: {line}')

                self.user_db_connection.commit()
                logger.debug(f'0.9.{patch} migration complete')
        else:
            logger.debug('user DB version is up to date')

        logger.info('END CHECK_FOR_UPDATES')

    def on_save_log_level(self, log_level):
        """
        Log level was changed by user, so we need to apply it on the spot and save to the user database.

        :param log_level:           new log level
        """
        self.logger.info('START ON_SAVE_AND_COMMIT_LOG_LEVEL')
        # In case logs were just enabled by the user and log file does not exist, create the log file
        if self.log_level >= LOG_LEVEL_OFF > log_level and not self.logger.hasHandlers():
            if not path.exists('logs'):
                mkdir('logs')

            current_datetime = datetime.now()
            logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                       .format(str(current_datetime.date()), current_datetime.time().hour,
                                               current_datetime.time().minute, current_datetime.time().second,
                                               current_datetime.time().microsecond))
            logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(logs_handler)
            self.logger.debug('created log file')

        # apply new log level to the main logger and save
        self.logger.setLevel(log_level)
        self.logger.debug(f'log level set up to {log_level} (was {self.log_level})')
        self.log_level = log_level
        self.user_db_cursor.execute('UPDATE log_options SET log_level = ?', (log_level, ))
        self.logger.debug(f'log level {self.log_level} saved')
        self.logger.info('END ON_SAVE_AND_COMMIT_LOG_LEVEL')
