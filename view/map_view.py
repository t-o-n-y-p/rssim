from pyglet.image import load
from pyglet.sprite import Sprite

from .view_base import View
from .button import ZoomInButton, ZoomOutButton


def _view_is_activated(fn):
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

        super().__init__(surface, batch, groups)
        self.main_map = load('img/map/4/full_map.png')
        self.main_map_sprite = None
        self.default_base_offset = (-3440, -1440)
        self.zoom_factor = 1.0
        self.zoom_in_button = ZoomInButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                           on_click_action=on_zoom_in_button)
        self.zoom_out_button = ZoomOutButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                             on_click_action=on_zoom_out_button)
        self.zoom_in_button.paired_button = self.zoom_out_button
        self.zoom_out_button.paired_button = self.zoom_in_button
        self.buttons.append(self.zoom_in_button)
        self.buttons.append(self.zoom_out_button)

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
            self.main_map_sprite = Sprite(self.main_map, x=self.default_base_offset[0], y=self.default_base_offset[1],
                                          batch=self.batch, group=self.groups['main_map'])
            self.main_map_sprite.opacity = 0

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.main_map_sprite.delete()
        self.main_map_sprite = None
        for b in self.buttons:
            b.on_deactivate()

    @_view_is_activated
    def on_change_base_offset(self, new_base_offset):
        self.main_map_sprite.position = new_base_offset

    def on_change_default_base_offset(self, new_default_base_offset):
        self.default_base_offset = new_default_base_offset

    def on_unlock_track(self, track_number):
        self.main_map = load(f'img/map/{track_number}/full_map.png')
        if self.is_activated:
            self.main_map_sprite.image = self.main_map

    def on_zoom_in(self):
        self.zoom_factor = 1.0
        if self.is_activated:
            self.main_map_sprite.scale = 1.0

    def on_zoom_out(self):
        self.zoom_factor = 0.5
        if self.is_activated:
            self.main_map_sprite.scale = 0.5

    def on_change_screen_resolution(self, screen_resolution):
        for b in self.buttons:
            b.on_position_changed((0, screen_resolution[1] - b.y_margin))
