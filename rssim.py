from ctypes import c_long, windll
from sys import exit
from sqlite3 import connect
from time import perf_counter

from pyglet import gl
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from win32api import MessageBoxEx
import win32con

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException
from game_objects import create_app


class RSSim:
    def __init__(self):
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise VideoAdapterNotSupportedException

        if windll.user32.GetSystemMetrics(0) < 1280 or windll.user32.GetSystemMetrics(1) < 720:
            raise MonitorNotSupportedException

        self.user_db_connection = connect('db/user.db')
        self.user_db_cursor = self.user_db_connection.cursor()
        self.config_db_connection = connect('db/config.db')
        self.config_db_cursor = self.config_db_connection.cursor()
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.batch = Batch()
        self.groups = {}
        numbered_groups = []
        for i in range(9):
            numbered_groups.append(OrderedGroup(i))

        self.groups['main_map'] = numbered_groups[0]
        self.groups['signal'] = numbered_groups[1]
        self.groups['train'] = numbered_groups[1]
        self.groups['boarding_light'] = numbered_groups[2]
        self.groups['twilight'] = numbered_groups[3]
        self.groups['twilight_artifacts'] = numbered_groups[4]
        self.groups['main_frame'] = numbered_groups[5]
        self.groups['tip'] = numbered_groups[6]
        self.groups['mini_map'] = numbered_groups[6]
        self.groups['game_progress_background'] = numbered_groups[6]
        self.groups['button_background'] = numbered_groups[7]
        self.groups['viewport_border'] = numbered_groups[7]
        self.groups['exp_money_time'] = numbered_groups[7]
        self.groups['button_text'] = numbered_groups[8]
        self.groups['button_border'] = numbered_groups[8]
        surface = Window(width=1280, height=720, caption='Railway Station Simulator', style='borderless',
                         fullscreen=False, vsync=False)
        self.surface = surface
        self.app = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                              config_db_cursor=self.config_db_cursor,
                              surface=self.surface, batch=self.batch, groups=self.groups)
        self.app.on_activate()
        self.app.on_change_screen_resolution(self.app.settings.model.screen_resolution,
                                             self.app.settings.model.fullscreen_mode)
        if self.app.settings.model.fullscreen_mode:
            self.app.on_fullscreen_mode_turned_on()

        @surface.event
        def on_draw():
            self.surface.clear()
            self.batch.draw()

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
