from abc import ABC, abstractmethod

from pyglet.sprite import Sprite as PygletSprite

from ui import *

SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X: Final = 150
SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y: Final = 100


def sprite_does_not_exist(fn):
    def _create_sprite_if_it_does_not_exist(*args, **kwargs):
        if args[0].sprite is None:
            fn(*args, **kwargs)

    return _create_sprite_if_it_does_not_exist


def sprite_exists(fn):
    def _delete_sprite_if_it_exists(*args, **kwargs):
        if args[0].sprite is not None:
            fn(*args, **kwargs)

    return _delete_sprite_if_it_exists


def texture_has_changed(fn):
    def _update_texture_if_it_has_changed(*args, **kwargs):
        if args[0].texture != args[1]:
            fn(*args, **kwargs)

    return _update_texture_if_it_has_changed


class Sprite(ABC):
    def __init__(self, logger):
        self.logger = logger
        self.sprite = None
        self.texture = None
        self.position = (0, 0)
        self.batch = None
        self.group = None
        self.usage = 'dynamic'
        self.subpixel = True
        self.opacity = 0
        self.rotation = 0
        self.scale = 1.0

    @abstractmethod
    def get_position(self):
        pass

    @final
    @sprite_does_not_exist
    def create(self):
        self.position = self.get_position()
        self.sprite = PygletSprite(self.texture, x=self.position[0], y=self.position[1], batch=self.batch,
                                   group=self.group, usage=self.usage, subpixel=self.subpixel)
        self.sprite.opacity = self.opacity
        self.sprite.update(rotation=self.rotation, scale=self.scale)

    @final
    @sprite_exists
    def delete(self):
        self.sprite.delete()
        self.sprite = None

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.sprite is not None:
            if self.opacity > 0:
                self.sprite.opacity = self.opacity
            else:
                self.delete()

    @final
    def on_position_changed(self):
        self.position = self.get_position()
        if self.sprite is not None:
            self.sprite.position = self.position

    @final
    @texture_has_changed
    def on_update_texture(self, new_texture):
        self.texture = new_texture
        if self.sprite is not None:
            self.sprite.image = self.texture

    @final
    def on_rotate(self, angle):
        self.rotation = angle
        if self.sprite is not None:
            self.sprite.rotation = angle


class UISprite(Sprite, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger=logger)
        self.parent_viewport = parent_viewport
        self.screen_resolution = (0, 0)

    @abstractmethod
    def get_scale(self):
        pass

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.position = self.get_position()
        self.scale = self.get_scale()
        if self.sprite is not None:
            self.sprite.update(x=self.position[0], y=self.position[1], scale=self.scale)


class MapSprite(Sprite, ABC):
    def __init__(self, map_id, logger, parent_viewport):
        super().__init__(logger=logger)
        self.map_id = map_id
        self.parent_viewport = parent_viewport

    @final
    def is_located_outside_viewport(self):
        return self.position[0] - self.texture.anchor_x \
               - (MAP_CAMERA.offset_x + self.parent_viewport.x2) / MAP_CAMERA.zoom \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or self.position[0] + self.texture.width - self.texture.anchor_x \
               - (MAP_CAMERA.offset_x + self.parent_viewport.x1) / MAP_CAMERA.zoom \
               < -SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or self.position[1] - self.texture.anchor_y \
               - (MAP_CAMERA.offset_y + self.parent_viewport.y2) / MAP_CAMERA.zoom \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y \
               or self.position[1] + self.texture.height - self.texture.anchor_y \
               - (MAP_CAMERA.offset_y + self.parent_viewport.y1) / MAP_CAMERA.zoom \
               < -SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y
