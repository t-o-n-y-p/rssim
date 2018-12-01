from ctypes import c_long
from sys import exit

from pyglet import gl
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from win32api import MessageBoxEx
import win32con

from game_config import GameConfig
from exceptions import VideoAdapterNotSupportedException
from game_objects import create_app


class RSSim:
    def __init__(self):
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise VideoAdapterNotSupportedException

        self.game_config = GameConfig()
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
        surface = Window(width=self.game_config.screen_resolution[0], height=self.game_config.screen_resolution[1],
                         caption='Railway Station Simulator', style='borderless', fullscreen=False,
                         vsync=self.game_config.vsync)
        self.surface = surface
        self.app_controller = create_app(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                         groups=self.groups)

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
