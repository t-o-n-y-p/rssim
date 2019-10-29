from logging import getLogger

from ui import *
from ui.button import UIButton


@final
class OpenMapSwitcherButton(UIButton):
    def __init__(self, on_click_action, on_hover_action, on_leave_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.open_map_switcher_button'),
                         parent_viewport=parent_viewport)
        self.transparent = False
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 40 / 80
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action

    def get_position(self):
        return ((self.parent_viewport.x1 + self.parent_viewport.x2) // 2
                - get_bottom_bar_height(self.screen_resolution) // 2,
                self.parent_viewport.y2 - 3 * get_top_bar_height(self.screen_resolution) // 2
                - get_bottom_bar_height(self.screen_resolution))

    def get_size(self):
        return (get_bottom_bar_height(self.screen_resolution),
                get_bottom_bar_height(self.screen_resolution))
