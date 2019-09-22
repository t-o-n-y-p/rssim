from logging import getLogger
from ctypes import c_char

from pyshaders import from_files_names
from pyglet.gl import *

from ui.shader_sprite import ShaderSprite
from ui import *


class TwilightShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.view.twilight_shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/twilight_view/shader.frag')
        self.group = GROUPS['twilight']
        self.height_map_uniform_name = (c_char * 10)()
        self.height_map_uniform_name.value = bytes('height_map', 'utf-8')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        glUniform1i(glGetUniformLocation(self.shader.pid, self.height_map_uniform_name), 0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.view.height_map.id)
        self.shader.uniforms.base_offset = self.view.base_offset
        self.shader.uniforms.scale = round(1 / self.view.zoom_factor)
        self.shader.uniforms.sun_phi_radians = self.view.current_sun_phi
        self.shader.uniforms.sun_theta_radians = self.view.current_sun_theta
        self.shader.uniforms.sun_brightness = self.view.current_sun_brightness
        self.shader.uniforms.sun_diffuse_brightness = self.view.current_diffuse_brightness
