from logging import getLogger

from button import Button


class CheckedCheckboxButton(Button):
    """
    Implements checked checkbox button.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.checked_checkbox_button'))
        self.to_activate_on_controller_init = False
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 42 / 80
        self.on_click_action = on_click_action