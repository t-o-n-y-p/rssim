from typing import final

from ui import get_top_bar_height, get_bottom_bar_height
from ui.button_v2 import UIButtonV2


@final
class BuildMapButtonV2(UIButtonV2):
    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 - get_top_bar_height(self.screen_resolution)

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 \
            - 5 * get_top_bar_height(self.screen_resolution) // 4

    def get_width(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_height(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_font_size(self):
        return int(40 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return ''
