from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


class ShopConstructorViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.shop.constructor.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/shop_constructor_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.shop_constructor_opacity = self.view.opacity
        self.shader.uniforms.shop_stages_cells_position = self.view.shop_stages_cells_position
        self.shader.uniforms.shop_stages_cells_size = self.view.shop_stages_cells_size
        self.shader.uniforms.current_stage = self.view.current_stage
        is_button_activated = []
        button_x = []
        button_y = []
        button_w = []
        button_h = []
        for b in self.view.buttons:
            is_button_activated.append(int(b.is_activated))
            button_x.append(b.position[0])
            button_y.append(b.position[1])
            button_w.append(b.button_size[0])
            button_h.append(b.button_size[1])

        self.shader.uniforms.is_button_activated = is_button_activated
        self.shader.uniforms.button_x = button_x
        self.shader.uniforms.button_y = button_y
        self.shader.uniforms.button_w = button_w
        self.shader.uniforms.button_h = button_h
        self.shader.uniforms.number_of_buttons = len(self.view.buttons)
