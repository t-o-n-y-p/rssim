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

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException, UpdateIncompatibleException
from rssim_core import *


class RSSim:
    """
    Makes game ready to play: creates app instance, checks for updates and implements main game loop.
    """
    def __init__(self):
        """
        Properties:
              user_db_connection        connection to the user DB (stores game state and user-defined settings)
              user_db_cursor            user DB cursor (is used to execute user DB queries)
              config_db_connection      connection to the config DB (stores all configuration
                                        that is not designed to be managed by user)
              config_db_cursor          configuration DB cursor (is used to execute configuration DB queries)
              logger                    main game logger
              log_level                 log level for base game logger
              surface                   surface to draw all UI objects on
              batches                   batches to group all labels and sprites
              groups                    defines drawing layers (some labels and sprites behind others)
              main_frame_shader         shader for main frame primitive (responsible for button borders,
                                        UI screens background, main app border)
              app                       App object, is responsible for high-level properties, UI and events
              notifications             list of all active system notifications
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
        # set blending mode; this is required to correctly draw transparent textures
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # create batches and groups for text labels, sprites and textures
        self.batches = {}
        numbered_batches = []
        for i in range(5):
            numbered_batches.append(Batch())

        self.batches['main_batch'] = numbered_batches[0]
        self.batches['mini_map_batch'] = numbered_batches[2]
        self.batches['main_frame'] = numbered_batches[3]
        self.batches['ui_batch'] = numbered_batches[4]
        self.groups = {}
        numbered_groups = []
        for i in range(12):
            numbered_groups.append(OrderedGroup(i))

        self.groups['environment'] = numbered_groups[0]
        self.groups['main_map'] = numbered_groups[1]
        self.groups['signal'] = numbered_groups[2]
        self.groups['train'] = numbered_groups[2]
        self.groups['boarding_light'] = numbered_groups[3]
        self.groups['environment_2'] = numbered_groups[4]
        self.groups['twilight'] = numbered_groups[5]
        self.groups['mini_environment'] = numbered_groups[6]
        self.groups['mini_map'] = numbered_groups[7]
        self.groups['mini_environment_2'] = numbered_groups[8]
        self.groups['main_frame'] = numbered_groups[9]
        self.groups['button_background'] = numbered_groups[10]
        self.groups['exp_money_time'] = numbered_groups[10]
        self.groups['button_text'] = numbered_groups[11]
        self.main_frame_shader = from_files_names('shaders/main_frame/shader.vert', 'shaders/main_frame/shader.frag')
        # create surface
        surface = Window(width=MIN_RESOLUTION_WIDTH, height=MIN_RESOLUTION_HEIGHT,
                         caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)
        self.surface = surface
        # flip the surface so user knows game has launched and is loading now
        self.surface.flip()
        # create App object
        self.app = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                              config_db_cursor=self.config_db_cursor,
                              surface=self.surface, batches=self.batches, groups=self.groups, loader=self)
        # initially app is created using default minimal screen resolution; now we change it to user resolution
        self.app.on_change_screen_resolution(self.app.settings.model.screen_resolution)
        # activate app after it is created
        self.app.on_activate()
        # and same about fullscreen mode
        if self.app.settings.model.fullscreen_mode and self.app.model.fullscreen_mode_available:
            self.app.on_fullscreen_mode_turned_on()

        self.notifications = []

        @surface.event
        def on_draw():
            """
            Implements on_draw event handler for surface. Handler is attached using @surface.event decoration.
            This handler clears surface and calls draw() function for all batches (inserts shaders if required)
            """
            # clear surface
            self.surface.clear()
            # draw main batch: environment, main map, signals, trains
            self.batches['main_batch'].draw()
            # draw mini map batch: mini map
            self.batches['mini_map_batch'].draw()
            # draw main frame batch with main frame shader: main app borders, button borders, UI screens background
            self.main_frame_shader.use()
            self.app.on_set_up_main_frame_shader_uniforms(self.main_frame_shader)
            self.batches['main_frame'].draw()
            self.main_frame_shader.clear()
            # draw ui batch: text labels, buttons
            self.batches['ui_batch'].draw()

        @surface.event
        def on_activate():
            """
            Implements on_activate event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it cannot send system notifications.
            Clears all queued notifications.
            """
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @surface.event
        def on_show():
            """
            Implements on_show event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it cannot send system notifications.
            Clears all queued notifications.
            """
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @surface.event
        def on_deactivate():
            """
            Implements on_deactivate event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it can send system notifications.
            """
            self.app.on_enable_notifications()

        @surface.event
        def on_hide():
            """
            Implements on_hide event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it can send system notifications.
            """
            self.app.on_enable_notifications()

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
            for h in self.app.on_mouse_press_handlers:
                h(x, y, button, modifiers)

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
            for h in self.app.on_mouse_release_handlers:
                h(x, y, button, modifiers)

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
            for h in self.app.on_mouse_motion_handlers:
                h(x, y, dx, dy)

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
            for h in self.app.on_mouse_drag_handlers:
                h(x, y, dx, dy, buttons, modifiers)

        @surface.event
        def on_mouse_leave(x, y):
            """
            Implements on_mouse_leave event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user moves the mouse cursor and it leaves the app window.
            This handler simply triggers all existing on_mouse_leave handlers (from buttons).

            :param x:               mouse cursor X position
            :param y:               mouse cursor Y position
            """
            for h in self.app.on_mouse_leave_handlers:
                h(x, y)

    def run(self):
        """
        Implements main game loop.
        """
        # fps_timer is used to determine if it's time to recalculate FPS
        fps_timer = 0.0
        while True:
            time_1 = perf_counter()
            # dispatch_events() launches keyboard and mouse handlers implemented above
            self.surface.dispatch_events()
            # increment in-game time
            self.app.game.on_update_time()
            # on_update_view() checks if all views content is up-to-date and opacity is correct
            self.app.on_update_view()
            # call on_draw() handler implemented above
            self.surface.dispatch_event('on_draw')
            # flip the surface so user can see all the game content
            self.surface.flip()
            time_4 = perf_counter()
            # FPS is recalculated every FPS_INTERVAL seconds
            if perf_counter() - fps_timer > FPS_INTERVAL:
                self.app.on_update_fps(round(float(1/(time_4 - time_1))))
                fps_timer = perf_counter()

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
            if user_db_version >= (0, 9, 4):
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
                raise UpdateIncompatibleException
        else:
            logger.debug('user DB version is up to date')

        logger.info('END CHECK_FOR_UPDATES')
