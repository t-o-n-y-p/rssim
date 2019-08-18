from ctypes import c_long, windll
from time import perf_counter
from os import path, mkdir
from logging import FileHandler, Formatter, getLogger
from datetime import datetime
from hashlib import sha512

from pyglet import gl
from keyring import get_password

from exceptions import *
from rssim_core import *
from ui import SURFACE, BATCHES, MIN_RESOLUTION_WIDTH, MIN_RESOLUTION_HEIGHT
from database import USER_DB_CURSOR, USER_DB_CONNECTION, on_commit


class RSSim:
    def __init__(self):
        # determine if video adapter supports all game textures, if not - raise specific exception
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < REQUIRED_TEXTURE_SIZE:
            raise VideoAdapterNotSupportedException

        # determine if screen resolution meets requirements, if not - raise specific exception
        if windll.user32.GetSystemMetrics(0) < MIN_RESOLUTION_WIDTH \
                or windll.user32.GetSystemMetrics(1) < MIN_RESOLUTION_HEIGHT:
            raise MonitorNotSupportedException

        with open('db/config.db', 'rb') as f1, open('db/default.db', 'rb') as f2:
            data = (f2.read() + f1.read())[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() != DATABASE_SHA512:
                raise HackingDetectedException

        with open('db/user.db', 'rb') as f:
            data = f.read()[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() \
                    != get_password(sha512('user_db'.encode('utf-8')).hexdigest(),
                                    sha512('user_db'.encode('utf-8')).hexdigest()):
                raise HackingDetectedException

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
        # create App object
        self.app = create_app(loader=self)
        # initially app is created using default minimal screen resolution; now we change it to user resolution
        # and same about fullscreen mode
        if self.app.model.fullscreen_mode and self.app.model.fullscreen_mode_available:
            self.app.on_fullscreen_mode_turned_on()

        # activate app after it is created
        self.app.fade_in_animation.on_activate()
        self.notifications = []

        @SURFACE.event
        def on_draw():
            # clear surface
            SURFACE.clear()
            for batch in BATCHES:
                BATCHES[batch].invalidate()

            # draw main batch: environment, main map, signals, trains
            BATCHES['main_batch'].draw()
            # draw mini map batch: mini map
            BATCHES['mini_map_batch'].draw()
            # draw all vertices with shaders
            self.app.on_apply_shaders_and_draw_vertices()
            # draw ui batch: text labels, buttons
            BATCHES['ui_batch'].draw()
            self.logger.debug(f'main_batch: {len(BATCHES["main_batch"]._draw_list)}')
            self.logger.debug(f'mini_map_batch: {len(BATCHES["mini_map_batch"]._draw_list)}')
            self.logger.debug(f'ui_batch: {len(BATCHES["ui_batch"]._draw_list)}')

        @SURFACE.event
        def on_activate():
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @SURFACE.event
        def on_show():
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @SURFACE.event
        def on_deactivate():
            self.app.on_enable_notifications()

        @SURFACE.event
        def on_hide():
            self.app.on_enable_notifications()

        @SURFACE.event
        def on_mouse_press(x, y, button, modifiers):
            for h in self.app.on_mouse_press_handlers:
                h(x, y, button, modifiers)

        @SURFACE.event
        def on_mouse_release(x, y, button, modifiers):
            for h in self.app.on_mouse_release_handlers:
                h(x, y, button, modifiers)

        @SURFACE.event
        def on_mouse_motion(x, y, dx, dy):
            for h in self.app.on_mouse_motion_handlers:
                h(x, y, dx, dy)

        @SURFACE.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            for h in self.app.on_mouse_drag_handlers:
                h(x, y, dx, dy, buttons, modifiers)

        @SURFACE.event
        def on_mouse_leave(x, y):
            for h in self.app.on_mouse_leave_handlers:
                h(x, y)

        @SURFACE.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            for h in self.app.on_mouse_scroll_handlers:
                h(x, y, scroll_x, scroll_y)

        @SURFACE.event
        def on_key_press(symbol, modifiers):
            for h in self.app.on_key_press_handlers:
                h(symbol, modifiers)

        @SURFACE.event
        def on_text(text):
            for h in self.app.on_text_handlers:
                h(text)

    def run(self):
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
            if user_db_version >= (0, 9, 7):
                logger.debug('upgrading database...')
                for patch in range(user_db_version[2] + 1, CURRENT_VERSION[2] + 1):
                    logger.debug(f'start 0.9.{patch} migration')
                    with open(f'db/patch/09{patch}.sql', 'r') as migration:
                        # simply execute each line in the migration script
                        for line in migration.readlines():
                            USER_DB_CURSOR.execute(line)
                            logger.debug(f'executed request: {line}')

                    on_commit()
                    logger.debug(f'0.9.{patch} migration complete')

            # update from versions < 0.9.7 is not supported
            else:
                raise UpdateIncompatibleException
        else:
            logger.debug('user DB version is up to date')

        logger.info('END CHECK_FOR_UPDATES')
