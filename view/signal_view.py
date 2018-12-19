from pyglet.image import load
from pyglet.sprite import Sprite

from .view_base import View


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def _signal_is_displayed_on_map(fn):
    def _handle_if_signal_is_displayed_on_map(*args, **kwargs):
        if args[0].signal_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_signal_is_displayed_on_map


class SignalView(View):
    def __init__(self, surface, batch, groups):
        super().__init__(surface, batch, groups)
        self.base_offset = (-3440, -1440)
        self.screen_resolution = (1280, 720)
        self.red_signal_image = load('img/signals/signal_red.png')
        self.green_signal_image = load('img/signals/signal_green.png')
        self.red_signal_image.anchor_x = 5
        self.red_signal_image.anchor_y = 5
        self.green_signal_image.anchor_x = 5
        self.green_signal_image.anchor_y = 5
        self.signal_sprite = None
        self.position = (0, 0)
        self.flip_needed = 0
        self.zoom_out_activated = False
        self.zoom_factor = 1.0
        self.state = None
        self.locked = None

    @_signal_is_displayed_on_map
    def on_update(self):
        if self.is_activated and self.signal_sprite.opacity < 255:
            self.signal_sprite.opacity += 15

        if not self.is_activated and self.signal_sprite is not None:
            if self.signal_sprite.opacity > 0:
                self.signal_sprite.opacity -= 15
                if self.signal_sprite.opacity <= 0:
                    self.signal_sprite.delete()
                    self.signal_sprite = None

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.signal_sprite is None and not self.locked:
            if self.state == 'red_signal':
                self.signal_sprite = Sprite(self.red_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batch,
                                            group=self.groups['signal'])
            else:
                self.signal_sprite = Sprite(self.green_signal_image, x=self.base_offset[0] + self.position[0],
                                            y=self.base_offset[1] + self.position[1], batch=self.batch,
                                            group=self.groups['signal'])

            if self.zoom_out_activated:
                self.signal_sprite.x = self.base_offset[0] + self.position[0] // 2
                self.signal_sprite.y = self.base_offset[1] + self.position[1] // 2

            self.signal_sprite.scale = self.zoom_factor
            if self.flip_needed == 1:
                self.signal_sprite.rotation = 180.0

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_unlock(self):
        self.signal_sprite = Sprite(self.red_signal_image, x=self.base_offset[0] + self.position[0],
                                    y=self.base_offset[1] + self.position[1], batch=self.batch,
                                    group=self.groups['signal'])
        if self.zoom_out_activated:
            self.signal_sprite.x = self.base_offset[0] + self.position[0] // 2
            self.signal_sprite.y = self.base_offset[1] + self.position[1] // 2

        self.signal_sprite.scale = self.zoom_factor
        if self.flip_needed == 1:
            self.signal_sprite.rotation = 180.0

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        if self.zoom_out_activated:
            x = self.base_offset[0] + self.position[0] // 2
            y = self.base_offset[1] + self.position[1] // 2
        else:
            x = self.base_offset[0] + self.position[0]
            y = self.base_offset[1] + self.position[1]

        if x not in range(-10, self.screen_resolution[0] + 10) or y not in range(-10, self.screen_resolution[1] + 10):
            if self.signal_sprite is not None:
                self.signal_sprite.delete()
                self.signal_sprite = None
        else:
            if self.signal_sprite is None:
                if not self.locked:
                    if self.state == 'red_signal':
                        self.signal_sprite = Sprite(self.red_signal_image, x=x, y=y, batch=self.batch,
                                                    group=self.groups['signal'])
                    else:
                        self.signal_sprite = Sprite(self.green_signal_image, x=x, y=y, batch=self.batch,
                                                    group=self.groups['signal'])

                    self.signal_sprite.scale = self.zoom_factor
                    if self.flip_needed == 1:
                        self.signal_sprite.rotation = 180.0
            else:
                self.signal_sprite.position = (x, y)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        if self.signal_sprite is not None:
            self.signal_sprite.scale = self.zoom_factor

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def on_change_state(self, state):
        self.state = state
        if self.signal_sprite is not None:
            if self.state == 'red_signal':
                self.signal_sprite.image = self.red_signal_image
            else:
                self.signal_sprite.image = self.green_signal_image
