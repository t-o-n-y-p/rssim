from logging import getLogger

from ui.button import Button


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
        self.base_font_size_property = 29 / 80
        self.on_click_action = on_click_action
