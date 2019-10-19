from logging import getLogger

from ui import *
from ui.button import UIButton


@final
class ZoomInButton(UIButton):
    def __init__(self, on_click_action, on_hover_action, on_leave_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.zoom_in_button'), parent_viewport=parent_viewport)
        self.transparent = False
        self.to_activate_on_controller_init = False
        self.text = '< >'
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action

    def get_position(self):
        return (self.parent_viewport.x1,
                self.parent_viewport.y2 - 3 * get_top_bar_height(self.screen_resolution) + 4)

    def get_size(self):
        return (2 * get_top_bar_height(self.screen_resolution) - 2,
                2 * get_top_bar_height(self.screen_resolution) - 2)
