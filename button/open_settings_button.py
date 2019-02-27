from logging import getLogger

from button import Button


class OpenSettingsButton(Button):
    """
    Implements Open settings button in the bottom right corner.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.open_settings_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.font_size = 30
        self.x_margin = 1200
        self.y_margin = 0
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
