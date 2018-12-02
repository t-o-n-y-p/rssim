from ctypes import c_long
from sys import exit
import sqlite3

from pyglet import gl
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from win32api import MessageBoxEx, GetSystemMetrics
import win32con

from exceptions import VideoAdapterNotSupportedException
from game_objects import create_app, create_game


class RSSim:
    def __init__(self):
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise VideoAdapterNotSupportedException

        self.user_db_connection = sqlite3.connect('db/user.db')
        self.user_db_cursor = self.user_db_connection.cursor()
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
        self.user_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = self.user_db_cursor.fetchall()
        i = 0
        while screen_resolution_config[i][0] <= GetSystemMetrics(0) \
                and screen_resolution_config[i][1] <= GetSystemMetrics(1) \
                and i < len(screen_resolution_config):
            i += 1

        fullscreen_resolution = screen_resolution_config[i - 1]
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics_config')
        fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics_config')
        windowed_resolution = self.user_db_cursor.fetchone()
        surface = None
        if fullscreen_mode:
            surface = Window(width=fullscreen_resolution[0], height=fullscreen_resolution[1],
                             caption='Railway Station Simulator', style='borderless', fullscreen=fullscreen_mode,
                             vsync=False)
        else:
            surface = Window(width=windowed_resolution[0], height=windowed_resolution[1],
                             caption='Railway Station Simulator', style='borderless', fullscreen=fullscreen_mode,
                             vsync=False)

        self.surface = surface
        self.app_controller = create_app(user_db_connection=self.user_db_connection, user_db_cursor=self.user_db_cursor,
                                         surface=self.surface, batch=self.batch, groups=self.groups)
        self.game_controller = create_game(user_db_connection=self.user_db_connection,
                                           user_db_cursor=self.user_db_cursor,
                                           surface=self.surface, batch=self.batch, groups=self.groups,
                                           parent_controller=self.app_controller)
        if fullscreen_mode:
            self.app_controller.on_change_screen_resolution(fullscreen_resolution, fullscreen_mode)
        else:
            self.app_controller.on_change_screen_resolution(windowed_resolution, fullscreen_mode)

        @surface.event
        def on_draw():
            self.surface.clear()
            self.batch.draw()

        @surface.event
        def on_mouse_press(x, y, button, modifiers):
            for h in self.app_controller.on_mouse_press_handlers:
                h(x, y, button, modifiers)

        @surface.event
        def on_mouse_release(x, y, button, modifiers):
            for h in self.app_controller.on_mouse_release_handlers:
                h(x, y, button, modifiers)

        @surface.event
        def on_mouse_motion(x, y, dx, dy):
            for h in self.app_controller.on_mouse_motion_handlers:
                h(x, y, dx, dy)

        @surface.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            for h in self.app_controller.on_mouse_drag_handlers:
                h(x, y, dx, dy, button, modifiers)

        @surface.event
        def on_mouse_leave(x, y):
            for h in self.app_controller.on_mouse_leave_handlers:
                h(x, y)

    def run(self):
        while True:
            self.surface.dispatch_events()
            self.app_controller.on_update_model()
            self.app_controller.on_update_view()
            self.surface.dispatch_event('on_draw')
            self.surface.flip()


def main():
    try:
        RSSim().run()
    except VideoAdapterNotSupportedException as e:
        MessageBoxEx(win32con.NULL, e.text, e.caption,
                     win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_DEFBUTTON1
                     | win32con.MB_SYSTEMMODAL | win32con.MB_SETFOREGROUND, 0)
        exit()


if __name__ == '__main__':
    main()
