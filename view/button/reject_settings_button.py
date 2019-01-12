from pyglet.image import load

from .button_base import Button


class RejectSettingsButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups)
        self.to_activate_on_controller_init = True
        self.vertex_list = None
        self.text_object = None
        self.text = ''
        self.font_name = 'Webdings'
        self.is_bold = False
        self.font_size = 40
        self.x_margin = 158
        self.y_margin = 720
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
