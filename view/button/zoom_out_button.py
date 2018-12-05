from pyglet.image import load

from .button_base import Button


class ZoomOutButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups)
        self.to_activate_on_controller_init = True
        self.border_sprite_image = load('img/button_borders/button_border_200_80.png')
        self.border_sprite = None
        self.vertex_list = None
        self.text_object = None
        self.text = '>> Zoom out <<'
        self.font_name = 'Arial'
        self.is_bold = False
        self.font_size = 16
        self.y_margin = 112
        self.button_size = (200, 80)
        self.on_click_action = on_click_action
