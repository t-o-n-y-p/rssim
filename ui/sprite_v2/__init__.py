from abc import ABC, abstractmethod
from typing import final, Final

from pyglet.sprite import Sprite as PygletSprite

from ui import MAP_CAMERA, window_size_has_changed, UIObject, is_not_active, is_active

SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X: Final = 150
SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y: Final = 100


def texture_has_changed(fn):
    def _update_texture_if_it_has_changed(*args, **kwargs):
        if args[0].texture != args[1]:
            fn(*args, **kwargs)

    return _update_texture_if_it_has_changed


class MapSpriteV2(UIObject, ABC):
    def __init__(self, map_id, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.map_id = map_id
        self.sprite = None
        self.texture = None
        self.batch = None
        self.group = None
        self.usage = 'dynamic'
        self.subpixel = True
        self.rotation = 0
        self.x = 0
        self.y = 0

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.sprite:
            self.sprite = PygletSprite(
                self.texture, x=self.x, y=self.y, batch=self.batch, group=self.group,
                usage=self.usage, subpixel=self.subpixel
            )

        self.sprite.opacity = self.opacity
        self.sprite.rotation = self.rotation

    @final
    def on_position_update(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
        if self.sprite:
            self.sprite.update(x=self.x, y=self.y, rotation=self.rotation)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        if self.sprite:
            if self.opacity > 0:
                self.sprite.opacity = self.opacity
            else:
                self.sprite.delete()
                self.sprite = None

    @final
    @texture_has_changed
    def on_update_texture(self, new_texture):
        self.texture = new_texture
        if self.sprite:
            self.sprite.image = self.texture

    @final
    def is_located_outside_viewport(self):
        return self.x - self.texture.anchor_x \
               - (MAP_CAMERA.offset_x + self.parent_viewport.x2) / MAP_CAMERA.zoom \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or self.x + self.texture.width - self.texture.anchor_x \
               - (MAP_CAMERA.offset_x + self.parent_viewport.x1) / MAP_CAMERA.zoom \
               < -SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or self.y - self.texture.anchor_y \
               - (MAP_CAMERA.offset_y + self.parent_viewport.y2) / MAP_CAMERA.zoom \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y \
               or self.y + self.texture.height - self.texture.anchor_y \
               - (MAP_CAMERA.offset_y + self.parent_viewport.y1) / MAP_CAMERA.zoom \
               < -SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y


class UISpriteV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.sprite = None
        self.texture = None
        self.batch = None
        self.group = None
        self.usage = 'dynamic'
        self.subpixel = True

    @abstractmethod
    def get_x(self):
        pass

    @abstractmethod
    def get_y(self):
        pass

    @abstractmethod
    def get_scale(self):
        pass

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.sprite:
            self.sprite = PygletSprite(
                self.texture, x=self.get_x(), y=self.get_y(), batch=self.batch, group=self.group,
                usage=self.usage, subpixel=self.subpixel
            )

        self.sprite.opacity = self.opacity
        self.sprite.scale = self.get_scale()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        if self.sprite:
            self.sprite.update(x=self.get_x(), y=self.get_y(), scale=self.get_scale())

    @final
    @is_active
    def on_position_changed(self):
        self.sprite.update(x=self.get_x(), y=self.get_y())
