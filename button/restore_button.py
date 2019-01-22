from button import Button


class RestoreButton(Button):
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups)
        self.to_activate_on_controller_init = False
        self.text = ''
        self.font_name = 'Webdings'
        self.is_bold = False
        self.font_size = 19
        self.x_margin = 1202
        self.y_margin = 680
        self.button_size = (40, 40)
        self.on_click_action = on_click_action
