from ctypes import c_long, windll
from sys import exit, exc_info
from sqlite3 import connect
from time import perf_counter
from os import path, mkdir
from shutil import copyfile
from logging import FileHandler, Formatter, getLogger
import datetime
from traceback import print_tb

from pyglet import gl
from pyglet import resource
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from win32api import MessageBoxEx
import win32con

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException
from rssimcore import create_app


current_version = (0, 9, 2)


class RSSim:
    def __init__(self):
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise VideoAdapterNotSupportedException

        if windll.user32.GetSystemMetrics(0) < 1280 or windll.user32.GetSystemMetrics(1) < 720:
            raise MonitorNotSupportedException

        if not path.exists('db/user.db'):
            copyfile('db/default.db', 'db/user.db')

        resource.path = ['font', 'img', 'img/main_map.zip']
        resource.reindex()
        self.user_db_connection = connect('db/user.db')
        self.user_db_cursor = self.user_db_connection.cursor()
        self.check_for_updates()
        self.config_db_connection = connect('db/config.db')
        self.config_db_cursor = self.config_db_connection.cursor()
        self.user_db_cursor.execute('SELECT log_level FROM log_options')
        self.log_level = self.user_db_cursor.fetchone()[0]
        self.logger = getLogger('root')
        current_datetime = datetime.datetime.now()
        if self.log_level < 30:
            if not path.exists('logs'):
                mkdir('logs')

            logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                       .format(str(current_datetime.date()), current_datetime.time().hour,
                                               current_datetime.time().minute, current_datetime.time().second,
                                               current_datetime.time().microsecond))
            logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(logs_handler)

        self.logger.setLevel(self.log_level)
        self.logger.debug('DB connection set up successfully')
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.logger.debug('blending set successfully')
        self.batches = {}
        numbered_batches = []
        for i in range(5):
            numbered_batches.append(Batch())

        self.batches['main_batch'] = numbered_batches[0]
        self.logger.debug('main batch created successfully')
        self.batches['main_frame'] = numbered_batches[3]
        self.logger.debug('main frame batch created successfully')
        self.batches['ui_batch'] = numbered_batches[4]
        self.logger.debug('ui batch created successfully')
        self.groups = {}
        numbered_groups = []
        for i in range(10):
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
        self.groups['car_skins'] = numbered_groups[3]
        self.logger.debug('car_skins group created successfully')
        self.groups['twilight'] = numbered_groups[4]
        self.logger.debug('twilight group created successfully')
        self.groups['mini_environment'] = numbered_groups[5]
        self.logger.debug('mini_environment group created successfully')
        self.groups['mini_map'] = numbered_groups[6]
        self.logger.debug('mini_map group created successfully')
        self.groups['main_frame'] = numbered_groups[7]
        self.logger.debug('main_frame group created successfully')
        self.groups['button_background'] = numbered_groups[8]
        self.logger.debug('button_background group created successfully')
        self.groups['exp_money_time'] = numbered_groups[8]
        self.logger.debug('exp_money_time group created successfully')
        self.groups['button_text'] = numbered_groups[9]
        self.logger.debug('button_text group created successfully')
        surface = Window(width=1280, height=720, caption='Railway Station Simulator', style='borderless',
                         fullscreen=False, vsync=False)
        self.logger.debug(f'surface {surface.width}x{surface.height} created successfully')
        self.surface = surface
        self.surface.flip()
        self.app = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                              config_db_cursor=self.config_db_cursor,
                              surface=self.surface, batches=self.batches, groups=self.groups, loader=self)
        self.logger.debug('app created successfully')
        self.app.on_activate()
        self.logger.debug('app activated successfully')
        self.app.on_change_screen_resolution(self.app.settings.model.screen_resolution,
                                             self.app.settings.model.fullscreen_mode)
        if self.app.settings.model.fullscreen_mode:
            self.app.on_fullscreen_mode_turned_on()

        @surface.event
        def on_draw():
            self.surface.clear()
            self.batches['main_batch'].draw()
            self.app.on_draw_main_frame()
            self.batches['ui_batch'].draw()

        @surface.event
        def on_mouse_press(x, y, button, modifiers):
            for h in self.app.on_mouse_press_handlers:
                h(x, y, button, modifiers)

        @surface.event
        def on_mouse_release(x, y, button, modifiers):
            for h in self.app.on_mouse_release_handlers:
                h(x, y, button, modifiers)

        @surface.event
        def on_mouse_motion(x, y, dx, dy):
            for h in self.app.on_mouse_motion_handlers:
                h(x, y, dx, dy)

        @surface.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            for h in self.app.on_mouse_drag_handlers:
                h(x, y, dx, dy, button, modifiers)

        @surface.event
        def on_mouse_leave(x, y):
            for h in self.app.on_mouse_leave_handlers:
                h(x, y)

    def run(self):
        fps_timer = 0.0
        while True:
            time_1 = perf_counter()
            self.surface.dispatch_events()
            self.app.game.on_update_time()
            self.app.on_update_view()
            self.surface.dispatch_event('on_draw')
            self.surface.flip()
            time_4 = perf_counter()
            if perf_counter() - fps_timer > 0.2:
                self.app.on_update_fps(round(float(1/(time_4 - time_1))))
                fps_timer = perf_counter()

    def check_for_updates(self):
        self.user_db_cursor.execute('SELECT * FROM sqlite_master WHERE type = "table" AND tbl_name = "version"')
        if len(self.user_db_cursor.fetchall()) == 0:
            self.user_db_cursor.execute('CREATE TABLE version (major integer, minor integer, patch integer)')
            self.user_db_cursor.execute('INSERT INTO version VALUES (0, 9, 1)')
            self.user_db_connection.commit()

        self.user_db_cursor.execute('SELECT * FROM version')
        if self.user_db_cursor.fetchone() < current_version:
            for patch in range(2, current_version[2] + 1):
                with open(f'db/patch/09{patch}.sql', 'r') as migration:
                    for line in migration.readlines():
                        self.user_db_cursor.execute(line)

                self.user_db_connection.commit()

    def on_save_and_commit_log_level(self, log_level):
        if self.log_level >= 30 > log_level:
            if not path.exists('logs'):
                mkdir('logs')

            current_datetime = datetime.datetime.now()
            logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                       .format(str(current_datetime.date()), current_datetime.time().hour,
                                               current_datetime.time().minute, current_datetime.time().second,
                                               current_datetime.time().microsecond))
            logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(logs_handler)

        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.user_db_cursor.execute('UPDATE log_options SET log_level = ?', (log_level, ))


def main():
    try:
        RSSim().run()
    except (VideoAdapterNotSupportedException, MonitorNotSupportedException) as e:
        MessageBoxEx(win32con.NULL, e.text, e.caption,
                     win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_DEFBUTTON1
                     | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND, 0)
    except Exception:
        crash_datetime = datetime.datetime.now()
        filename = 'logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.crash'\
            .format(str(crash_datetime.date()), crash_datetime.time().hour,
                    crash_datetime.time().minute, crash_datetime.time().second,
                    crash_datetime.time().microsecond)
        with open(filename, 'w') as crash_dump:
            crash_dump.write('Traceback (most recent call last):\n')
            print_tb(exc_info()[2], file=crash_dump)
            crash_dump.write('{}: {}\n'.format(exc_info()[0].__name__, exc_info()[1]))
    finally:
        exit()


if __name__ == '__main__':
    main()
