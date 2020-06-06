from typing import final

from ui import get_top_bar_height
from ui.button_v2 import UIButtonV2


@final
class BuildShopStageButtonV2(UIButtonV2):
    def get_x(self):
        return self.parent_viewport.x2 - 3 * get_top_bar_height(self.screen_resolution) // 2

    def get_y(self):
        return self.parent_viewport.y1 + 9 * get_top_bar_height(self.screen_resolution) // 8

    def get_width(self):
        return get_top_bar_height(self.screen_resolution)

    def get_height(self):
        return get_top_bar_height(self.screen_resolution)

    def get_font_size(self):
        return int(40 / 80 * get_top_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return ''
