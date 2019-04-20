from logging import getLogger

from ui.button import Button


class CloseLicenseButton(Button):
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.close_license_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 24 / 80
        self.on_click_action = on_click_action