from abc import ABC, abstractmethod
from inspect import getfullargspec
from typing import final, Final

from pyglet.sprite import Sprite as PygletSprite

from ui import MAP_CAMERA, window_size_has_changed, UIObject, is_not_active, is_active

SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X: Final = 150
SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y: Final = 100


def _create_sprite(cls, parent_object):
    sprite_name_snake_case = ''.join('_' + c.lower() if c.isupper() else c for c in cls.__name__).lstrip('_')
    cls_resource_keys = getfullargspec(cls).args[3:]
    parent_object.__setattr__(
        sprite_name_snake_case,
        cls(
            parent_object.logger.getChild(sprite_name_snake_case), parent_object.parent_viewport,
            *(parent_object.__getattribute__(a) for a in cls_resource_keys)
        )
    )
    sprite_object = parent_object.__getattribute__(sprite_name_snake_case)
    parent_object.ui_objects.append(sprite_object)
    parent_object.fade_out_animation.child_animations.append(sprite_object.fade_out_animation)
    parent_object.on_window_resize_handlers.extend(sprite_object.on_window_resize_handlers)
    return sprite_object


def default_sprite(cls):
    def _default_sprite(f):
        def _add_default_sprite(*args, **kwargs):
            f(*args, **kwargs)
            if issubclass(cls, (UISpriteV2, MapSpriteV2)):
                sprite_object = _create_sprite(cls, args[0])
                args[0].fade_in_animation.child_animations.append(sprite_object.fade_in_animation)

        return _add_default_sprite

    return _default_sprite


def sprite(cls):
    def _sprite(f):
        def _add_sprite(*args, **kwargs):
            f(*args, **kwargs)
            if issubclass(cls, (UISpriteV2, MapSpriteV2)):
                _create_sprite(cls, args[0])

        return _add_sprite

    return _sprite


def texture_has_changed(f):
    def _update_texture_if_it_has_changed(*args, **kwargs):
        if args[0].texture != args[1]:
            f(*args, **kwargs)

    return _update_texture_if_it_has_changed


class SpriteV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.sprite = None
        self.texture = None
        self.batch = None
        self.group = None
        self.usage = 'dynamic'
        self.subpixel = True

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


class MapSpriteV2(SpriteV2, ABC):
    def __init__(self, logger, parent_viewport, map_id):
        super().__init__(logger, parent_viewport)
        self.map_id = map_id
        self.rotation = 0
        self.x = 0
        self.y = 0

    @final
    def on_update(self):
        if not self.sprite and self.is_located_inside_viewport():
            self.sprite = PygletSprite(
                self.texture, x=self.x, y=self.y, batch=self.batch, group=self.group,
                usage=self.usage, subpixel=self.subpixel
            )
            self.sprite.opacity = self.opacity
            self.sprite.rotation = self.rotation
        elif self.is_located_outside_viewport() and self.sprite:
            self.sprite.delete()
            self.sprite = None

    @final
    def on_position_update(self, x=0, y=0, rotation=0):
        self.x = x
        self.y = y
        self.rotation = rotation
        if self.sprite:
            self.sprite.update(x=self.x, y=self.y, rotation=self.rotation)

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

    @final
    def is_located_inside_viewport(self):
        return not self.is_located_outside_viewport()


class UISpriteV2(SpriteV2, ABC):
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
    def on_position_update(self):
        self.sprite.update(x=self.get_x(), y=self.get_y())
