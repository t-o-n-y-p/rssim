from ctypes import c_long, windll
from os import path, mkdir
from typing import Final, final
from hashlib import sha512
from logging import FileHandler, Formatter, getLogger
from datetime import datetime
from sqlite3 import OperationalError
from time import perf_counter

import pyglet
from keyring import get_password
from pyglet import gl

from database import USER_DB_LOCATION, USER_DB_CURSOR, on_commit
from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException, HackingDetectedException, \
    UpdateIncompatibleException
from ui import MIN_RESOLUTION_WIDTH, MIN_RESOLUTION_HEIGHT, WINDOW, BATCHES, MAP_CAMERA
from controller.app_controller import AppController


def video_adapter_is_supported(fn):
    def _launch_game_if_video_adapter_is_supported(*args, **kwargs):
        # determine if video adapter supports all game textures, if not - raise specific exception
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < REQUIRED_TEXTURE_SIZE:
            raise VideoAdapterNotSupportedException

        fn(*args, **kwargs)

    return _launch_game_if_video_adapter_is_supported


def monitor_is_supported(fn):
    def _launch_game_if_monitor_is_supported(*args, **kwargs):
        # determine if screen resolution meets requirements, if not - raise specific exception
        if windll.user32.GetSystemMetrics(0) < MIN_RESOLUTION_WIDTH \
                or windll.user32.GetSystemMetrics(1) < MIN_RESOLUTION_HEIGHT:
            raise MonitorNotSupportedException

        fn(*args, **kwargs)

    return _launch_game_if_monitor_is_supported


def game_config_was_not_modified(fn):
    def _launch_game_if_game_config_was_not_modified(*args, **kwargs):
        with open('db/config.db', 'rb') as f1, open('db/default.db', 'rb') as f2:
            data = (f2.read() + f1.read())[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() != DATABASE_SHA512:
                raise HackingDetectedException

            fn(*args, **kwargs)

    return _launch_game_if_game_config_was_not_modified


def player_progress_was_not_modified(fn):
    def _launch_game_if_player_progress_was_not_modified(*args, **kwargs):
        with open(path.join(USER_DB_LOCATION, 'user.db'), 'rb') as f:
            data = f.read()[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() \
                    != get_password(sha512('user_db'.encode('utf-8')).hexdigest(),
                                    sha512('user_db'.encode('utf-8')).hexdigest()):
                raise HackingDetectedException

            fn(*args, **kwargs)

    return _launch_game_if_player_progress_was_not_modified


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 10, 3)                    # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 10, 3)      # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = '2f7833b8cf58a4ef67535647626ad8da7381df24aa2fc1726623e25da347a81b0c414ee92154f449564ccde72e02db0207ce89f2ba72d53599565891390bdf66'
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_SCROLL_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------


@final
class Launcher:
    @video_adapter_is_supported
    @monitor_is_supported
    @game_config_was_not_modified
    @player_progress_was_not_modified
    def __init__(self):
        def on_app_update(dt):
            # increment in-game time
            self.app.game.on_update_time()
            # on_update_view() checks if all views content is up-to-date and opacity is correct
            self.app.on_update_view()

        # check if game was updated from previous version (0.9.0 and higher are supported)
        self.on_check_for_updates()
        # set up the main logger, create log file
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
        self.app = AppController(loader=self)
        # activate app after it is created
        self.app.fade_in_animation.on_activate()
        pyglet.clock.schedule(on_app_update)
        self.on_mouse_motion_event_counter = 0
        self.on_mouse_motion_cached_movement = [0, 0]
        self.on_mouse_drag_event_counter = 0
        self.on_mouse_drag_cached_movement = [0, 0]
        self.on_mouse_scroll_event_counter = 0
        self.on_mouse_scroll_cached_movement = [0, 0]
        self.last_frame_time = perf_counter()

        @WINDOW.event
        def on_draw():
            # clear surface
            WINDOW.clear()
            for batch in BATCHES:
                BATCHES[batch].invalidate()

            # draw main batch: environment, main map, signals, trains
            with MAP_CAMERA:
                BATCHES['main_batch'].draw()

            # draw mini map batch: mini map
            BATCHES['mini_map_batch'].draw()
            # draw all vertices with shaders
            self.app.on_apply_shaders_and_draw_vertices()
            # draw ui batch: text labels, buttons
            BATCHES['ui_batch'].draw()
            self.on_mouse_motion_event_counter = 0
            self.on_mouse_drag_event_counter = 0
            self.on_mouse_scroll_event_counter = 0
            # while perf_counter() - self.last_frame_time < 1/60:
            #     pass
            #
            # self.last_frame_time = perf_counter()

        @WINDOW.event
        def on_activate():
            for h in self.app.on_window_activate_handlers:
                h()

        @WINDOW.event
        def on_show():
            for h in self.app.on_window_show_handlers:
                h()

        @WINDOW.event
        def on_deactivate():
            for h in self.app.on_window_deactivate_handlers:
                h()

        @WINDOW.event
        def on_hide():
            for h in self.app.on_window_hide_handlers:
                h()

        @WINDOW.event
        def on_mouse_press(x, y, button, modifiers):
            for h in self.app.on_mouse_press_handlers:
                h(x, y, button, modifiers)

        @WINDOW.event
        def on_mouse_release(x, y, button, modifiers):
            for h in self.app.on_mouse_release_handlers:
                h(x, y, button, modifiers)

        @WINDOW.event
        def on_mouse_motion(x, y, dx, dy):
            if self.on_mouse_motion_event_counter < MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME:
                self.on_mouse_motion_event_counter += 1
                dx += self.on_mouse_motion_cached_movement[0]
                dy += self.on_mouse_motion_cached_movement[1]
                self.on_mouse_motion_cached_movement = [0, 0]
                for h in self.app.on_mouse_motion_handlers:
                    h(x, y, dx, dy)

            else:
                self.on_mouse_motion_cached_movement[0] += dx
                self.on_mouse_motion_cached_movement[1] += dy

        @WINDOW.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            if self.on_mouse_drag_event_counter < MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME:
                self.on_mouse_drag_event_counter += 1
                dx += self.on_mouse_drag_cached_movement[0]
                dy += self.on_mouse_drag_cached_movement[1]
                self.on_mouse_drag_cached_movement = [0, 0]
                for h in self.app.on_mouse_drag_handlers:
                    h(x, y, dx, dy, buttons, modifiers)

            else:
                self.on_mouse_drag_cached_movement[0] += dx
                self.on_mouse_drag_cached_movement[1] += dy

        @WINDOW.event
        def on_mouse_leave(x, y):
            for h in self.app.on_mouse_leave_handlers:
                h(x, y)

        @WINDOW.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            if self.on_mouse_scroll_event_counter < MAXIMUM_MOUSE_SCROLL_EVENTS_PER_FRAME:
                self.on_mouse_scroll_event_counter += 1
                scroll_x += self.on_mouse_scroll_cached_movement[0]
                scroll_y += self.on_mouse_scroll_cached_movement[1]
                self.on_mouse_scroll_cached_movement = [0, 0]
                for h in self.app.on_mouse_scroll_handlers:
                    h(x, y, scroll_x, scroll_y)

            else:
                self.on_mouse_scroll_cached_movement[0] += scroll_x
                self.on_mouse_scroll_cached_movement[1] += scroll_y

        @WINDOW.event
        def on_key_press(symbol, modifiers):
            for h in self.app.on_key_press_handlers:
                h(symbol, modifiers)

        @WINDOW.event
        def on_text(text):
            for h in self.app.on_text_handlers:
                h(text)

        @WINDOW.event
        def on_resize(width, height):
            for h in self.app.on_window_resize_handlers:
                h(width, height)

    @staticmethod
    def run():
        pyglet.app.run()

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
        # If version exists, read it from user DB.
        # If current game version is higher, use migration scripts one by one.
        # Migration script file is named "<version>.sql"
        try:
            USER_DB_CURSOR.execute('SELECT * FROM version')
        except OperationalError:
            raise UpdateIncompatibleException

        user_db_version = USER_DB_CURSOR.fetchone()
        logger.debug(f'user DB version: {user_db_version}')
        logger.debug(f'current game version: {CURRENT_VERSION}')
        if user_db_version == CURRENT_VERSION:
            logger.debug('user DB version is up to date')
        # update from versions < MIN_UPDATE_COMPATIBLE_VERSION is not supported
        elif user_db_version < MIN_UPDATE_COMPATIBLE_VERSION:
            raise UpdateIncompatibleException
        else:
            logger.debug('upgrading database...')
            next_app_version = [*user_db_version[MAJOR:PATCH], user_db_version[PATCH] + 1]
            while next_app_version <= list(CURRENT_VERSION):
                if path.exists('db/patch/{}{}{}.sql'.format(*next_app_version)):
                    logger.debug('start {}.{}.{} migration'.format(*next_app_version))
                    with open('db/patch/{}{}{}.sql'.format(*next_app_version), 'r') as migration:
                        # simply execute each line in the migration script
                        for line in migration.readlines():
                            USER_DB_CURSOR.execute(line)
                            logger.debug(f'executed request: {line}')

                    on_commit()
                    logger.debug('{}.{}.{} migration complete'.format(*next_app_version))
                    next_app_version[PATCH] += 1
                else:
                    next_app_version[MINOR] += 1
                    next_app_version[PATCH] = 0
                    if not path.exists('db/patch/{}{}{}.sql'.format(*next_app_version)):
                        next_app_version[MAJOR] += 1
                        next_app_version[MINOR], next_app_version[PATCH] = 0, 0

            logger.debug('user DB version is up to date')

        logger.info('END CHECK_FOR_UPDATES')
