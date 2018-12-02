from .view_base import View
from pyglet.image import load
from pyglet.sprite import Sprite


def _view_is_activated(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


class MapView(View):
    def __init__(self, surface, batch, groups):
        super().__init__(surface, batch, groups)
        self.main_map = load('img/map/4/full_map.png')
        self.main_map_sprite = None
        self.default_base_offset = (-3440, -1440)

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

    def on_deactivate(self):
        self.is_activated = False

    @_view_is_activated
    def on_change_base_offset(self, new_base_offset):
        self.main_map_sprite.position = new_base_offset

    def on_change_default_base_offset(self, new_default_base_offset):
        self.default_base_offset = new_default_base_offset

    def on_unlock_track(self, track_number):
        self.main_map = load(f'img/map/{track_number}/full_map.png')
        if self.is_activated:
            self.main_map_sprite.image = self.main_map
