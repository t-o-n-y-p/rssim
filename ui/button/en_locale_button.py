from logging import getLogger

from ui.button import Button


class ENLocaleButton(Button):
    """
    Implements EN locale button in the top bar.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.en_locale_button'))
        self.to_activate_on_controller_init = True
        self.text = ' '
        self.font_name = 'Arial'
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action
