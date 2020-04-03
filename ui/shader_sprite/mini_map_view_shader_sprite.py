from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


@final
class MiniMapViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.mini_map.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/mini_map_view/shader.frag')

    def get_bottom_edge(self):
        return 0.0

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.mini_map_opacity = self.view.opacity
        self.shader.uniforms.mini_map_position_size = (
            *get_mini_map_position(self.screen_resolution),
            get_mini_map_width(self.screen_resolution), get_mini_map_height(self.screen_resolution)
        )
        self.shader.uniforms.mini_map_frame_position_size = (
            *self.view.get_mini_map_frame_position(),
            self.view.get_mini_map_frame_width(), self.view.get_mini_map_frame_height()
        )
