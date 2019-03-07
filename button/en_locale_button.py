from logging import getLogger

from button import Button


class ENLocaleButton(Button):
    """
    Implements EN locale button in the top bar.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.en_locale_button'))
        self.to_activate_on_controller_init = True
        self.text = ' '
        self.font_name = 'Arial'
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action
