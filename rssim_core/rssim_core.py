from ctypes import c_long, windll
from time import perf_counter
from os import path, mkdir
from logging import FileHandler, Formatter, getLogger
from datetime import datetime

from pyglet import gl

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException, UpdateIncompatibleException
from rssim_core import *
from ui import SURFACE, BATCHES, MIN_RESOLUTION_WIDTH, MIN_RESOLUTION_HEIGHT
from database import USER_DB_CURSOR, USER_DB_CONNECTION


class RSSim:
    """
    Makes game ready to play: creates app instance, checks for updates and implements main game loop.
    """
    def __init__(self):
        """
        Properties:
              logger                    main game logger
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

        # check if game was updated from previous version (0.9.0 and higher are supported)
        self.on_check_for_updates()
        # set up the main logger; if logs are turned on, create log file
        # USER_DB_CURSOR.execute('SELECT log_level FROM log_options')
        # self.log_level = USER_DB_CURSOR.fetchone()[0]
        self.logger = getLogger('root')
        current_datetime = datetime.now()
        if not path.exists('logs'):
            mkdir('logs')

        logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                   .format(str(current_datetime.date()), current_datetime.time().hour,
                                           current_datetime.time().minute, current_datetime.time().second,
                                           current_datetime.time().microsecond),
                                   encoding='utf8')
        logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)
        self.logger.setLevel(LOG_LEVEL_DEBUG)
        # set blending mode; this is required to correctly draw transparent textures
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # flip the surface so user knows game has launched and is loading now
        SURFACE.flip()
        # create App object
        self.app = create_app(loader=self)
        # initially app is created using default minimal screen resolution; now we change it to user resolution
        # and same about fullscreen mode
        if self.app.model.fullscreen_mode and self.app.model.fullscreen_mode_available:
            self.app.on_fullscreen_mode_turned_on()

        # activate app after it is created
        self.app.on_activate_view()
        self.notifications = []

        @SURFACE.event
        def on_draw():
            """
            Implements on_draw event handler for surface. Handler is attached using @surface.event decoration.
            This handler clears surface and calls draw() function for all batches (inserts shaders if required)
            """
            # clear surface
            SURFACE.clear()
            # draw main batch: environment, main map, signals, trains
            BATCHES['main_batch'].draw()
            # draw mini map batch: mini map
            BATCHES['mini_map_batch'].draw()
            # draw all vertices with shaders
            self.app.on_apply_shaders_and_draw_vertices()
            # draw ui batch: text labels, buttons
            BATCHES['ui_batch'].draw()

        @SURFACE.event
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

        @SURFACE.event
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

        @SURFACE.event
        def on_deactivate():
            """
            Implements on_deactivate event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it can send system notifications.
            """
            self.app.on_enable_notifications()

        @SURFACE.event
        def on_hide():
            """
            Implements on_hide event handler for surface. Handler is attached using @surface.event decoration.
            This handler notifies the app that it can send system notifications.
            """
            self.app.on_enable_notifications()

        @SURFACE.event
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

        @SURFACE.event
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

        @SURFACE.event
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

        @SURFACE.event
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

        @SURFACE.event
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

        @SURFACE.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            """
            Implements on_mouse_scroll event handler for surface. Handler is attached using @surface.event decoration.
            Event is fired when user scrolls the mouse wheel.
            This handler simply triggers all existing on_mouse_scroll handlers.

            :param x:               mouse cursor X position
            :param y:               mouse cursor Y position
            :param scroll_x:        number of “clicks” the horizontal wheel moved
            :param scroll_y:        number of “clicks” the vertical wheel moved
            """
            for h in self.app.on_mouse_scroll_handlers:
                h(x, y, scroll_x, scroll_y)

    def run(self):
        """
        Implements main game loop.
        """
        # fps_timer is used to determine if it's time to recalculate FPS
        fps_timer = 0.0
        while True:
            time_1 = perf_counter()
            # dispatch_events() launches keyboard and mouse handlers implemented above
            SURFACE.dispatch_events()
            # increment in-game time
            self.app.game.on_update_time()
            # on_update_view() checks if all views content is up-to-date and opacity is correct
            self.app.on_update_view()
            # call on_draw() handler implemented above
            SURFACE.dispatch_event('on_draw')
            # flip the surface so user can see all the game content
            SURFACE.flip()
            time_4 = perf_counter()
            # FPS is recalculated every FPS_INTERVAL seconds
            if perf_counter() - fps_timer > FPS_INTERVAL:
                self.app.on_update_fps(round(float(1/(time_4 - time_1))))
                fps_timer = perf_counter()

    @staticmethod
    def on_check_for_updates():
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
        USER_DB_CURSOR.execute('SELECT * FROM sqlite_master WHERE type = "table" AND tbl_name = "version"')
        if len(USER_DB_CURSOR.fetchall()) == 0:
            logger.debug('version info not found')
            USER_DB_CURSOR.execute('CREATE TABLE version (major integer, minor integer, patch integer)')
            logger.debug('version table created')
            USER_DB_CURSOR.execute('INSERT INTO version VALUES (0, 9, 1)')
            logger.debug('version 0.9.1 set')
            USER_DB_CONNECTION.commit()

        # If version exists, read it from user DB.
        # If current game version is higher, use migration scripts one by one.
        # Migration script file is named "<version>.sql"
        USER_DB_CURSOR.execute('SELECT * FROM version')
        user_db_version = USER_DB_CURSOR.fetchone()
        logger.debug(f'user DB version: {user_db_version}')
        logger.debug(f'current game version: {CURRENT_VERSION}')
        if user_db_version < CURRENT_VERSION:
            if user_db_version >= (0, 9, 6):
                logger.debug('upgrading database...')
                for patch in range(user_db_version[2] + 1, CURRENT_VERSION[2] + 1):
                    logger.debug(f'start 0.9.{patch} migration')
                    with open(f'db/patch/09{patch}.sql', 'r') as migration:
                        # simply execute each line in the migration script
                        for line in migration.readlines():
                            USER_DB_CURSOR.execute(line)
                            logger.debug(f'executed request: {line}')

                    USER_DB_CONNECTION.commit()
                    logger.debug(f'0.9.{patch} migration complete')
            # update from versions < 0.9.6 is not supported
            else:
                raise UpdateIncompatibleException
        else:
            logger.debug('user DB version is up to date')

        logger.info('END CHECK_FOR_UPDATES')
