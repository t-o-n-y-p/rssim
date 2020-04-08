from abc import ABC, abstractmethod
from typing import final

from pyglet.gl import GL_QUADS

from ui import window_size_has_changed, GROUPS, BATCHES


def shader_sprite_does_not_exist(fn):
    def _create_shader_sprite_if_it_does_not_exist(*args, **kwargs):
        if args[0].sprite is None:
            fn(*args, **kwargs)

    return _create_shader_sprite_if_it_does_not_exist


def shader_sprite_exists(fn):
    def _delete_shader_sprite_if_it_exists(*args, **kwargs):
        if args[0].sprite is not None:
            fn(*args, **kwargs)

    return _delete_shader_sprite_if_it_exists


class ShaderSprite(ABC):
    def __init__(self, logger, view):
        self.logger = logger
        self.view = view
        self.shader = None
        self.sprite = None
        self.bottom_edge = -1.0
        self.top_edge = 1.0
        self.batch = BATCHES['main_frame']
        self.group = GROUPS['main_frame']
        self.screen_resolution = (0, 0)
        self.opacity = 0

    @abstractmethod
    def get_bottom_edge(self):
        pass

    @abstractmethod
    def get_top_edge(self):
        pass

    @abstractmethod
    def set_uniforms(self):
        pass

    @final
    @shader_sprite_does_not_exist
    def create(self):
        self.sprite = self.batch.add(
            4, GL_QUADS, self.group,
            ('v2f/static', (-1.0, self.bottom_edge, -1.0, self.top_edge, 1.0, self.top_edge, 1.0, self.bottom_edge))
        )

    @final
    @shader_sprite_exists
    def delete(self):
        self.sprite.delete()
        self.sprite = None

    @final
    @shader_sprite_exists
    def draw(self):
        self.shader.use()
        self.set_uniforms()
        self.sprite.draw(GL_QUADS)
        self.shader.clear()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.bottom_edge = self.get_bottom_edge()
        self.top_edge = self.get_top_edge()
        if self.sprite is not None:
            self.sprite.vertices = (
                -1.0, self.bottom_edge, -1.0, self.top_edge, 1.0, self.top_edge, 1.0, self.bottom_edge
            )

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            self.delete()
