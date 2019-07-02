from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite


class OnboardingViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.onboarding.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/onboarding_view/shader.frag')

    def get_bottom_edge(self):
        return -1.0

    def get_top_edge(self):
        return 1.0

    def set_uniforms(self):
        self.shader.uniforms.onboarding_opacity = self.view.opacity
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
