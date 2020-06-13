from abc import ABC, abstractmethod
from typing import final

from pyglet.sprite import Sprite

from ui import window_size_has_changed, GROUPS, BATCHES, UIObject, is_not_active


class RectangleProgressBarV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.inactive_image = None
        self.inactive_sprite = None
        self.active_image = None
        self.active_sprite = None
        self.current_percent = 0

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_scale(self):
        pass

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.inactive_sprite:
            self.inactive_sprite = Sprite(
                self.inactive_image, x=self.viewport.x1, y=self.viewport.y1,
                batch=BATCHES['ui_batch'], group=GROUPS['button_background']
            )

        self.inactive_sprite.scale = self.get_scale()
        self.inactive_sprite.opacity = self.opacity
        if self.current_percent == 0:
            image_region = self.active_image.get_region(
                self.active_image.height // 2, self.active_image.height // 2, 1, 1
            )
        else:
            image_region = self.active_image.get_region(
                0, 0, self.current_percent * self.active_image.width // 100, self.active_image.height
            )

        if not self.active_sprite:
            self.active_sprite = Sprite(
                image_region, x=self.viewport.x1, y=self.viewport.y1,
                batch=BATCHES['ui_batch'], group=GROUPS['button_text']
            )
        else:
            self.active_sprite.image = image_region

        self.active_sprite.scale = self.get_scale()
        self.active_sprite.opacity = self.opacity

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1, self.viewport.y1 = self.get_position()
        self.viewport.x2 = self.viewport.x1 + int(self.inactive_image.width * self.get_scale())
        self.viewport.y2 = self.viewport.y1 + int(self.inactive_image.height * self.get_scale())
        if self.inactive_sprite:
            self.inactive_sprite.position = (self.viewport.x1, self.viewport.y1)
            self.inactive_sprite.scale = self.get_scale()

        if self.active_sprite:
            self.active_sprite.position = (self.viewport.x1, self.viewport.y1)
            self.active_sprite.scale = self.get_scale()

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            if self.inactive_sprite:
                self.inactive_sprite.delete()
                self.inactive_sprite = None

            if self.active_sprite:
                self.active_sprite.delete()
                self.active_sprite = None
        else:
            if self.inactive_sprite:
                self.inactive_sprite.opacity = self.opacity

            if self.active_sprite:
                self.active_sprite.opacity = self.opacity

    @final
    def on_update_progress_bar_state(self, current_value, maximum_value):
        if maximum_value == 0:
            self.current_percent = 0
        else:
            self.current_percent = int(current_value / maximum_value * 100)
            if self.current_percent > 100:
                self.current_percent = 100

        if self.is_activated:
            if self.current_percent == 0:
                self.active_sprite.image = self.active_image.get_region(
                    self.active_image.height // 2, self.active_image.height // 2, 1, 1
                )
            else:
                self.active_sprite.image = self.active_image.get_region(
                    0, 0, self.current_percent * self.active_image.width // 100, self.active_image.height
                )
