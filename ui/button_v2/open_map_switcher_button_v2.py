from typing import final

from ui import get_bottom_bar_height, get_top_bar_height
from ui.button_v2 import UIButtonV2


@final
class OpenMapSwitcherButtonV2(UIButtonV2):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.transparent = False

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
