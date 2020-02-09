from os import mkdir
from logging import FileHandler, Formatter, getLogger
from datetime import datetime
from sqlite3 import OperationalError
from time import perf_counter
from typing import final

import pyglet

from exceptions import UpdateIncompatibleException
from rssim_core import *
from ui import WINDOW, BATCHES, MAP_CAMERA
from database import USER_DB_CURSOR, on_commit
from controller.app_controller import AppController


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
        self.notifications = []
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
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @WINDOW.event
        def on_show():
            self.app.on_disable_notifications()
            for h in self.notifications:
                h.destroy()

            self.notifications.clear()

        @WINDOW.event
        def on_deactivate():
            self.app.on_enable_notifications()

        @WINDOW.event
        def on_hide():
            self.app.on_enable_notifications()

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
            for h in self.app.on_resize_handlers:
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
            while next_app_version <= CURRENT_VERSION:
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
