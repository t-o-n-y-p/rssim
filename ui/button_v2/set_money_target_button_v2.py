from typing import final

from ui import get_bottom_bar_height
from ui.button_v2 import UIButtonV2


@final
class SetMoneyTargetButtonV2(UIButtonV2):
    def get_x(self):
        return self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution) * 2 + 2

    def get_y(self):
        return self.parent_viewport.y1

    def get_font_size(self):
        return int(40 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return ''

    def get_width(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_height(self):
        return get_bottom_bar_height(self.screen_resolution)
