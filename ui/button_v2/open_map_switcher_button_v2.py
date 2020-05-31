from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, get_top_bar_height
from ui.button_v2 import UIButtonV2


@final
class OpenMapSwitcherButtonV2(UIButtonV2):
    def __init__(self, on_click_action, on_hover_action, on_leave_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.open_map_switcher_button'), parent_viewport=parent_viewport)
        self.transparent = False
        self.font_name = 'Webdings'
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
            - get_bottom_bar_height(self.screen_resolution) // 2

    def get_y(self):
        return self.parent_viewport.y2 - 3 * get_top_bar_height(self.screen_resolution) // 2 \
            - get_bottom_bar_height(self.screen_resolution)

    def get_width(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_height(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_font_size(self):
        return int(48 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return ''
