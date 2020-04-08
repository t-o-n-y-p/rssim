from logging import getLogger
from typing import final

from pyshaders import from_files_names

from ui import get_top_bar_height, get_bottom_bar_height
from ui.shader_sprite import ShaderSprite


@final
class SchedulerViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.scheduler.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/scheduler_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.screen_resolution = self.screen_resolution
        self.shader.uniforms.schedule_opacity = self.view.opacity
