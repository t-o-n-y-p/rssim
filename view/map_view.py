from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import mouse

from .view_base import View
from .button import ZoomInButton, ZoomOutButton


def _map_move_mode_available(fn):
    def _turn_on_move_mode_if_map_move_mode_available(*args, **kwargs):
        if args[0].map_move_mode_available:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_available


def _map_move_mode_enabled(fn):
    def _turn_on_move_mode_if_map_move_mode_enabled(*args, **kwargs):
        if args[0].map_move_mode:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_enabled


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


class MapView(View):
    def __init__(self, surface, batch, groups):
        def on_zoom_in_button(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_in()

        def on_zoom_out_button(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_out()

        def on_leave_action():
            self.map_move_mode_available = True

        def on_hover_action():
            self.map_move_mode_available = False

        super().__init__(surface, batch, groups)
        self.main_map = load('img/map/4/full_map.png')
        self.main_map_sprite = None
        self.screen_resolution = (1280, 720)
        self.base_offset = (-3440, -1440)
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (-6880, -2880)
        self.zoom_factor = 1.0
        self.zoom_out_activated = False
        self.zoom_in_button = ZoomInButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                           on_click_action=on_zoom_in_button, on_hover_action=on_hover_action,
                                           on_leave_action=on_leave_action)
        self.zoom_out_button = ZoomOutButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                             on_click_action=on_zoom_out_button, on_hover_action=on_hover_action,
                                             on_leave_action=on_leave_action)
        self.zoom_in_button.paired_button = self.zoom_out_button
        self.zoom_out_button.paired_button = self.zoom_in_button
        self.buttons.append(self.zoom_in_button)
        self.buttons.append(self.zoom_out_button)
        self.map_move_mode_available = True
        self.map_move_mode = False
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    def on_update(self):
        if self.is_activated and self.main_map_sprite.opacity < 255:
            self.main_map_sprite.opacity += 15

        if not self.is_activated and self.main_map_sprite is not None:
            if self.main_map_sprite.opacity > 0:
                self.main_map_sprite.opacity -= 15
                if self.main_map_sprite.opacity <= 0:
                    self.main_map_sprite.delete()
                    self.main_map_sprite = None

    def on_activate(self):
        self.is_activated = True
        if self.main_map_sprite is None:
            self.main_map_sprite = Sprite(self.main_map, x=self.base_offset[0], y=self.base_offset[1],
                                          batch=self.batch, group=self.groups['main_map'])
            self.main_map_sprite.opacity = 0
            self.main_map_sprite.scale = self.zoom_factor

        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.main_map_sprite.delete()
        self.main_map_sprite = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.check_base_offset_limits()
        if self.is_activated:
            self.main_map_sprite.position = self.base_offset

    def on_unlock_track(self, track_number):
        self.main_map = load(f'img/map/{track_number}/full_map.png')
        if self.is_activated:
            self.main_map_sprite.image = self.main_map

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        if self.is_activated:
            self.main_map_sprite.scale = zoom_factor

        if zoom_out_activated:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - 4080, self.screen_resolution[1] - 1800)
            self.on_change_base_offset((self.base_offset[0] // 2 + self.screen_resolution[0] // 4,
                                        self.base_offset[1] // 2 + self.screen_resolution[1] // 4))
        else:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - 8160, self.screen_resolution[1] - 3600)
            self.on_change_base_offset((self.base_offset[0] * 2 - self.screen_resolution[0] // 2,
                                        self.base_offset[1] * 2 - self.screen_resolution[1] // 2))

    def on_change_screen_resolution(self, screen_resolution):
        self.base_offset_upper_right_limit = (screen_resolution[0] - 8160, screen_resolution[1] - 3600)
        self.on_change_base_offset((self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                                    self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2))
        self.screen_resolution = screen_resolution
        for b in self.buttons:
            b.on_position_changed((0, screen_resolution[1] - b.y_margin))

    @_left_button
    @_view_is_active
    @_map_move_mode_available
    def handle_mouse_press(self, x, y, button, modifiers):
        self.map_move_mode = True

    @_map_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.controller.on_change_base_offset((self.base_offset[0] + dx, self.base_offset[1] + dy))

    @_left_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.map_move_mode = False

    def check_base_offset_limits(self):
        if self.base_offset[0] > self.base_offset_lower_left_limit[0]:
            self.base_offset = (self.base_offset_lower_left_limit[0], self.base_offset[1])

        if self.base_offset[0] < self.base_offset_upper_right_limit[0]:
            self.base_offset = (self.base_offset_upper_right_limit[0], self.base_offset[1])

        if self.base_offset[1] > self.base_offset_lower_left_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_lower_left_limit[1])

        if self.base_offset[1] < self.base_offset_upper_right_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_upper_right_limit[1])
