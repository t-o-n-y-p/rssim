from logging import getLogger
from typing import final

from pyshaders import from_files_names

from ui import get_bottom_bar_height, get_top_bar_height
from ui.shader_sprite import ShaderSprite


@final
class GameViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/game_view/shader.frag')

    def get_bottom_edge(self):
        return -1.0

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.screen_resolution = self.view.screen_resolution
        self.shader.uniforms.bottom_bar_height = get_bottom_bar_height(self.view.screen_resolution)
        self.shader.uniforms.game_frame_opacity = self.view.opacity
        self.shader.uniforms.is_button_activated = [int(self.view.open_map_switcher_button.is_activated), ]
        self.shader.uniforms.button_x = [self.view.open_map_switcher_button.position[0], ]
        self.shader.uniforms.button_y = [self.view.open_map_switcher_button.position[1], ]
        self.shader.uniforms.button_w = [self.view.open_map_switcher_button.button_size[0], ]
        self.shader.uniforms.button_h = [self.view.open_map_switcher_button.button_size[1], ]
        self.shader.uniforms.number_of_buttons = 1
