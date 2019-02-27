from logging import getLogger

from button import Button


class FullscreenButton(Button):
    """
    Implements middle button in the top right corner (in windowed mode).
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.fullscreen_button'))
        self.to_activate_on_controller_init = False
        self.text = ''
        self.font_name = 'Webdings'
        self.font_size = 19
        self.x_margin = 1202
        self.y_margin = 680
        self.button_size = (40, 40)
        self.on_click_action = on_click_action
