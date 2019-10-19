from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


@final
class OnboardingPageControlShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.onboarding.view.onboarding_page_control.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/onboarding_page_control/shader.frag')

    def get_bottom_edge(self):
        return get_inner_area_rect(self.screen_resolution)[1] / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        inner_area_rect = get_inner_area_rect(self.screen_resolution)
        return (inner_area_rect[1] + inner_area_rect[3]) / self.screen_resolution[1] * 2 - 1

    def set_uniforms(self):
        self.shader.uniforms.onboarding_page_control_opacity = self.view.opacity
        self.shader.uniforms.position = (self.view.pages[self.view.current_page].viewport.x1,
                                         self.view.pages[self.view.current_page].viewport.y1)
        self.shader.uniforms.size = (self.view.pages[self.view.current_page].viewport.x2
                                     - self.view.pages[self.view.current_page].viewport.x1,
                                     self.view.pages[self.view.current_page].viewport.y2
                                     - self.view.pages[self.view.current_page].viewport.y1)
        self.shader.uniforms.page_number = self.view.current_page
