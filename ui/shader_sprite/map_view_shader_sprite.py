from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


class MapViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/map_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.map_opacity = self.view.opacity
        self.shader.uniforms.is_button_activated \
            = [int(self.view.zoom_in_button.is_activated or self.view.zoom_out_button.is_activated), ]
        self.shader.uniforms.button_x \
            = [self.view.zoom_in_button.position[0], ]
        self.shader.uniforms.button_y \
            = [self.view.zoom_in_button.position[1], ]
        self.shader.uniforms.button_w \
            = [self.view.zoom_in_button.button_size[0], ]
        self.shader.uniforms.button_h \
            = [self.view.zoom_in_button.button_size[1], ]
        self.shader.uniforms.number_of_buttons = 1
        self.shader.uniforms.mini_map_opacity = self.view.mini_map_opacity
        self.shader.uniforms.mini_map_position_size = (self.view.mini_map_position[0], self.view.mini_map_position[1],
                                                       self.view.mini_map_width, self.view.mini_map_height)
        self.shader.uniforms.mini_map_frame_position_size \
            = (self.view.mini_map_frame_position[0], self.view.mini_map_frame_position[1],
               self.view.mini_map_frame_width, self.view.mini_map_frame_height)
