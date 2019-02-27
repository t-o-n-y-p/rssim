from logging import getLogger

from button import Button


class IconifyGameButton(Button):
    """
    Implements first button in the top right corner.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.iconify_game_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.font_size = 19
        self.x_margin = 1164
        self.y_margin = 680
        self.button_size = (40, 40)
        self.on_click_action = on_click_action
