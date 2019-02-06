from logging import getLogger

from button import Button


class CloseConstructorButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.close_constructor_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.is_bold = False
        self.font_size = 24
        self.x_margin = 0
        self.y_margin = 0
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
