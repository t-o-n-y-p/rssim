from .button_base import Button


class ZoomInButton(Button):
    def __init__(self, surface, batch, groups, on_click_action, on_hover_action, on_leave_action):
        super().__init__(surface, batch, groups)
        self.transparent = False
        self.to_activate_on_controller_init = False
        self.vertex_list = None
        self.text_object = None
        self.text = '< >'
        self.font_name = 'Perfo'
        self.is_bold = True
        self.font_size = 30
        self.x_margin = 0
        self.y_margin = 602
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action
