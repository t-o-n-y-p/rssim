from logging import getLogger

from ui.button import Button


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
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action
