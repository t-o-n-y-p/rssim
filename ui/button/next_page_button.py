from logging import getLogger

from ui.button import Button


class NextPageButton(Button):
    """
    Implements "next" button for license_page controls.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.next_page_button'))
        self.to_activate_on_controller_init = False
        self.text = '►'
        self.font_name = 'Arial'
        self.base_font_size_property = 32 / 80
        self.on_click_action = on_click_action
