from pyglet.image import load

from .button_base import Button


class BuyTrackButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups)
        self.to_activate_on_controller_init = False
        self.border_sprite_image = load('img/button_borders/button_border_80_80.png')
        self.border_sprite = None
        self.vertex_list = None
        self.text_object = None
        self.text = ''
        self.font_name = 'Webdings'
        self.font_size = 40
        self.x_margin = 691
        self.y_margin = 535
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
