from logging import getLogger

from ui.button import Button


class ZoomOutButton(Button):
    """
    Implements Zoom out button for game map on main game screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action, on_hover_action, on_leave_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.zoom_out_button'))
        self.transparent = False
        self.to_activate_on_controller_init = False
        self.text = '> <'
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action
