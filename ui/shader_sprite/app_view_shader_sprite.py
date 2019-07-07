from logging import getLogger

from pyshaders import from_files_names

from ui import *
from ui.shader_sprite import ShaderSprite


class AppViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/app_view/shader.frag')

    def get_bottom_edge(self):
        return -1.0

    def get_top_edge(self):
        return 1.0

    def set_uniforms(self):
        self.shader.uniforms.screen_resolution = self.view.screen_resolution
        self.shader.uniforms.top_bar_height = get_top_bar_height(self.view.screen_resolution)
        self.shader.uniforms.opacity = self.view.opacity
