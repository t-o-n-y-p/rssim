from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


@final
class ShopViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.shop.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/shop_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.shop_window_opacity = self.view.opacity
        self.shader.uniforms.shop_window_position = (self.view.viewport.x1, self.view.viewport.y1)
        self.shader.uniforms.shop_window_size = (
            self.view.viewport.x2 - self.view.viewport.x1,
            self.view.viewport.y2 - self.view.viewport.y1
        )
        self.shader.uniforms.top_bar_height = get_top_bar_height(self.screen_resolution)
