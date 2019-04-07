from logging import getLogger

from ui.button import Button


class CheckedCheckboxButton(Button):
    """
    Implements checked checkbox button.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.checked_checkbox_button'))
        self.to_activate_on_controller_init = False
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 42 / 80
        self.on_click_action = on_click_action
