from abc import ABC
from typing import final

from pyglet.gl import GL_QUADS
from pyglet.graphics import OrderedGroup

from ui import get_bottom_bar_height, window_size_has_changed, UIObject, localizable, is_not_active, BATCHES


class OnboardingPageV2(UIObject, ABC):
    @localizable
    def __init__(self, logger, parent_viewport, shader):
        super().__init__(logger, parent_viewport)
        self.shader = shader
        self.shader_group = OnboardingPageGroup(order=10, page=self)
        self.shader_sprite = None

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.shader_sprite:
            self.shader_sprite = BATCHES['ui_batch'].add(
                4, GL_QUADS, self.shader_group,
                ('v2i/static', (
                    self.viewport.x1, self.viewport.y1, self.viewport.mid_x, self.viewport.y1,
                    self.viewport.mid_x, self.viewport.y2, self.viewport.x1, self.viewport.y2
                ))
            )

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1, self.viewport.x2 = self.parent_viewport.x1, self.parent_viewport.x2
        self.viewport.y1 = self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
        self.viewport.y2 = self.parent_viewport.y2
        if self.shader_sprite:
            self.shader_sprite.vertices = (
                self.viewport.x1, self.viewport.y1, self.viewport.mid_x, self.viewport.y1,
                self.viewport.mid_x, self.viewport.y2, self.viewport.x1, self.viewport.y2
            )

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        if self.opacity <= 0 and self.shader_sprite:
            self.shader_sprite.delete()
            self.shader_sprite = None


@final
class OnboardingPageGroup(OrderedGroup):
    def __init__(self, order, page):
        super().__init__(order)
        self.page = page

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self.order == other.order and self.page == other.page

    def set_state(self):
        self.page.shader.use()
        self.page.shader.uniforms.page_opacity = self.page.opacity
        self.page.shader.uniforms.page_viewport_position = (self.page.viewport.x1, self.page.viewport.y1)
        self.page.shader.uniforms.page_viewport_size = (self.page.viewport.width // 2, self.page.viewport.height // 2)

    def unset_state(self):
        self.page.shader.clear()
