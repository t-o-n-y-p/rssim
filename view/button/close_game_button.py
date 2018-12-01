from .button_base import Button
from pyglet.image import load


class CloseGameButton(Button):
    def __init__(self, game_config, surface, batch, groups, on_click_action):
        super().__init__(game_config, surface, batch, groups)
        self.to_activate_on_controller_init = True
        self.border_sprite_image = load('img/button_borders/button_border_34_34.png')
        self.border_sprite = None
        self.vertex_list = None
        self.text_object = None
        self.text = ''
        self.font_name = 'Webdings'
        self.is_bold = False
        self.font_size = 16
        self.x_margin = 34
        self.y_margin = 34
        self.position = (self.game_config.screen_resolution[0] - self.x_margin,
                         self.game_config.screen_resolution[1] - self.y_margin)
        self.button_size = (34, 34)
        self.on_click_action = on_click_action
