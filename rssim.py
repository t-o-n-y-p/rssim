from ctypes import c_long, windll
from sys import exit
from sqlite3 import connect
from time import perf_counter
from os import path, mkdir
from shutil import copyfile
from logging import FileHandler, Formatter, getLogger
import datetime

from pyglet import gl
from pyglet import resource
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from win32api import MessageBoxEx
import win32con

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException
from rssimcore import create_app


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

        if not path.exists('logs'):
            mkdir('logs')

        self.logger = getLogger('game')
        current_datetime = datetime.datetime.now()
        logs_handler = FileHandler('logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.log'
                                   .format(str(current_datetime.date()), current_datetime.time().hour,
                                           current_datetime.time().minute, current_datetime.time().second,
                                           current_datetime.time().microsecond))
        logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)

        resource.path = ['font', 'img', 'img/main_map.zip']
        resource.reindex()
        self.user_db_connection = connect('db/user.db')
        self.user_db_cursor = self.user_db_connection.cursor()
        self.check_for_updates()
        self.config_db_connection = connect('db/config.db')
        self.config_db_cursor = self.config_db_connection.cursor()
        self.user_db_cursor.execute('SELECT log_level FROM log_options')
        self.logger.setLevel(self.user_db_cursor.fetchone()[0])
        self.logger.critical('DB connection set up successfully')
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.batch = Batch()
        self.main_frame_batch = Batch()
        self.ui_batch = Batch()
        self.groups = {}
        numbered_groups = []
        for i in range(10):
            numbered_groups.append(OrderedGroup(i))

        self.groups['environment'] = numbered_groups[0]
        self.groups['main_map'] = numbered_groups[1]
        self.groups['signal'] = numbered_groups[2]
        self.groups['train'] = numbered_groups[2]
        self.groups['boarding_light'] = numbered_groups[3]
        self.groups['car_skins'] = numbered_groups[3]
        self.groups['twilight'] = numbered_groups[4]
        self.groups['mini_environment'] = numbered_groups[5]
        self.groups['mini_map'] = numbered_groups[6]
        self.groups['main_frame'] = numbered_groups[7]
        self.groups['button_background'] = numbered_groups[8]
        self.groups['exp_money_time'] = numbered_groups[8]
        self.groups['button_text'] = numbered_groups[9]
        surface = Window(width=1280, height=720, caption='Railway Station Simulator', style='borderless',
                         fullscreen=False, vsync=False)
        self.surface = surface
        self.surface.flip()
        self.app = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                              config_db_cursor=self.config_db_cursor,
                              surface=self.surface, batch=self.batch, main_frame_batch=self.main_frame_batch,
                              ui_batch=self.ui_batch, groups=self.groups)
        self.app.on_activate()
        self.app.on_change_screen_resolution(self.app.settings.model.screen_resolution,
                                             self.app.settings.model.fullscreen_mode)
        if self.app.settings.model.fullscreen_mode:
            self.app.on_fullscreen_mode_turned_on()

        @surface.event
        def on_draw():
            self.surface.clear()
            self.batch.draw()
            self.app.on_draw_main_frame()
            self.ui_batch.draw()

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
        if self.user_db_cursor.fetchone() < (0, 9, 2):
            self.user_db_cursor.execute('CREATE TABLE log_options (log_level integer)')
            self.user_db_cursor.execute('INSERT INTO log_options VALUES (50)')
            self.user_db_cursor.execute('UPDATE version SET major = 0, minor = 9, patch = 2')
            self.user_db_connection.commit()


def main():
    try:
        RSSim().run()
    except (VideoAdapterNotSupportedException, MonitorNotSupportedException) as e:
        MessageBoxEx(win32con.NULL, e.text, e.caption,
                     win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_DEFBUTTON1
                     | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND, 0)
        exit()


if __name__ == '__main__':
    main()
