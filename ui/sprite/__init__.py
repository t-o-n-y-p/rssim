from typing import Final, final

import pyglet.sprite

from database import USER_DB_CURSOR


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


class Sprite:
    def __init__(self, logger):
        self.logger = logger
        self.sprite = None
        self.texture = None
        self.position = (0, 0)
        self.batch = None
        self.group = None
        self.usage = 'dynamic'
        self.subpixel = False
        self.opacity = 0
        self.rotation = 0
        self.scale = 1.0

    def get_position(self):
        pass

    @final
    @sprite_does_not_exist
    def create(self):
        self.position = self.get_position()
        self.sprite = pyglet.sprite.Sprite(self.texture, x=self.position[0], y=self.position[1], batch=self.batch,
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


class UISprite(Sprite):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger=logger)
        self.parent_viewport = parent_viewport
        self.screen_resolution = (1280, 720)

    def get_scale(self):
        pass

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.position = self.get_position()
        self.scale = self.get_scale()
        if self.sprite is not None:
            self.sprite.update(x=self.position[0], y=self.position[1], scale=self.scale)


class MapSprite(Sprite):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger=logger)
        self.parent_viewport = parent_viewport
        USER_DB_CURSOR.execute('SELECT last_known_base_offset FROM graphics')
        self.base_offset = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        USER_DB_CURSOR.execute('SELECT zoom_out_activated FROM graphics')
        self.zoom_out_activated = bool(USER_DB_CURSOR.fetchone()[0])
        if self.zoom_out_activated:
            self.scale = 0.5
        else:
            self.scale = 1.0

    @final
    def on_change_base_offset(self, base_offset):
        self.base_offset = base_offset
        self.on_position_changed()

    @final
    def on_change_scale(self, new_scale):
        self.scale = new_scale
        if self.sprite is not None:
            self.sprite.scale = self.scale

    @final
    def is_located_outside_viewport(self):
        return self.parent_viewport.x1 - (self.position[0] + (self.texture.width - self.texture.anchor_x) * self.scale)\
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or (self.position[0] - self.texture.anchor_x * self.scale) - self.parent_viewport.x2 \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_X \
               or self.parent_viewport.y1 \
               - (self.position[1] + (self.texture.height - self.texture.anchor_y) * self.scale) \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y \
               or (self.position[1] - self.texture.anchor_y * self.scale) - self.parent_viewport.y2 \
               > SPRITE_VIEWPORT_EDGE_OFFSET_LIMIT_Y
