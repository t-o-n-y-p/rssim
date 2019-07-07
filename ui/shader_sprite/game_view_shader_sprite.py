from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


class GameViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/game_view/shader.frag')

    def get_bottom_edge(self):
        return -1.0

    def get_top_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def set_uniforms(self):
        self.shader.uniforms.screen_resolution = self.view.screen_resolution
        self.shader.uniforms.bottom_bar_height = get_bottom_bar_height(self.view.screen_resolution)
        self.shader.uniforms.game_frame_opacity = self.view.opacity
