from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import mouse
from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW

from .view_base import View
from .button import CloseGameButton, IconifyGameButton, FullscreenButton, RestoreButton


def _game_window_is_active(fn):
    def _handle_if_game_window_is_active(*args, **kwargs):
        if args[0].surface.visible:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_active


def _game_is_not_fullscreen(fn):
    def _handle_if_game_window_is_not_fullscreen(*args, **kwargs):
        if not args[0].surface.fullscreen:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_not_fullscreen


def _app_window_move_mode_enabled(fn):
    def _handle_if_app_window_move_mode_enabled(*args, **kwargs):
        if args[0].app_window_move_mode:
            fn(*args, **kwargs)

    return _handle_if_app_window_move_mode_enabled


def _left_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


class AppView(View):
    def __init__(self, surface, batch, groups):
        def on_close_game(button):
            self.controller.on_close_game()

        def on_iconify_game(button):
            self.surface.minimize()

        def on_app_window_fullscreen(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_fullscreen_mode_turned_on()

        def on_app_window_restore(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_fullscreen_mode_turned_off()

        super().__init__(surface, batch, groups)
        self.main_frame = load('img/main_frame/main_frame_1280_720.png')
        self.main_frame_sprite = None
        self.buttons.append(CloseGameButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                            on_click_action=on_close_game))
        self.buttons.append(IconifyGameButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                              on_click_action=on_iconify_game))
        self.fullscreen_button = FullscreenButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                  on_click_action=on_app_window_fullscreen)
        self.restore_button = RestoreButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                            on_click_action=on_app_window_restore)
        self.fullscreen_button.paired_button = self.restore_button
        self.restore_button.paired_button = self.fullscreen_button
        self.buttons.append(self.fullscreen_button)
        self.buttons.append(self.restore_button)
        self.app_window_move_mode = False
        self.app_window_move_offset = (0, 0)
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    def on_update(self):
        if self.is_activated and self.main_frame_sprite.opacity < 255:
            self.main_frame_sprite.opacity += 15

        if not self.is_activated and self.main_frame_sprite is not None:
            if self.main_frame_sprite.opacity > 0:
                self.main_frame_sprite.opacity -= 15
                if self.main_frame_sprite.opacity <= 0:
                    self.main_frame_sprite.delete()
                    self.main_frame_sprite = None

    def on_activate(self):
        self.is_activated = True
        if self.main_frame_sprite is None:
            self.main_frame_sprite = Sprite(self.main_frame, x=0, y=0, batch=self.batch,
                                            group=self.groups['main_frame'])
            self.main_frame_sprite.opacity = 0

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution, fullscreen):
        if not fullscreen:
            self.surface.set_size(screen_resolution[0], screen_resolution[1])

        self.main_frame = load('img/main_frame/main_frame_{}_{}.png'.format(screen_resolution[0], screen_resolution[1]))
        if self.is_activated:
            self.main_frame_sprite.image = self.main_frame

        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))

    def on_fullscreen_mode_turned_on(self):
        self.surface.set_fullscreen(fullscreen=True)

    def on_fullscreen_mode_turned_off(self):
        self.surface.set_fullscreen(fullscreen=False)

    @_game_window_is_active
    @_game_is_not_fullscreen
    @_left_button
    @_view_is_active
    def handle_mouse_press(self, x, y, button, modifiers):
        y = self.surface.height - y
        if x in range(0, self.surface.width - 100) and y in range(0, 33):
            self.app_window_move_mode = True
            self.app_window_move_offset = (x, y)

    @_game_window_is_active
    @_left_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.app_window_move_mode = False

    @_game_window_is_active
    @_app_window_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.absolute_mouse_pos = GetCursorPos()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        SetWindowPos(self.game_window_handler, HWND_TOP,
                     self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                     self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                     self.game_window_position[2] - self.game_window_position[0],
                     self.game_window_position[3] - self.game_window_position[1], SWP_NOREDRAW)
