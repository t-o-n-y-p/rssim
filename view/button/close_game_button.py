from pyglet.image import load

from .button_base import Button


class CloseGameButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups)
        self.to_activate_on_controller_init = True
        self.border_sprite_image = load('img/button_borders/button_border_34_34.png')
        self.border_sprite = None
        self.vertex_list = None
        self.text_object = None
        self.text = ''
        self.font_name = 'Webdings'
        self.is_bold = False
        self.font_size = 18
        self.x_margin = 40
        self.y_margin = 40
        self.button_size = (40, 40)
        self.on_click_action = on_click_action
