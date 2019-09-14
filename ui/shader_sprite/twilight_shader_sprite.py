from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


class TwilightShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.view.twilight_shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/twilight_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.twilight_opacity = self.view.opacity
        self.shader.uniforms.base_offset = self.view.base_offset
