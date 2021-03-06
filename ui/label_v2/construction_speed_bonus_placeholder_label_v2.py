from typing import final

from ui import get_bottom_bar_height, YELLOW_GREY_RGB
from ui.label_v2 import LabelV2


@final
class ConstructionSpeedBonusPlaceholderLabelV2(LabelV2):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = YELLOW_GREY_RGB
        self.anchor_x = 'center'

    def get_x(self):
        bonus_label_window_width \
            = self.parent_viewport.x2 - 6 * get_bottom_bar_height(self.screen_resolution) + 2 \
            - 3 * get_bottom_bar_height(self.screen_resolution) // 16 \
            - (self.parent_viewport.x1 + 9 * get_bottom_bar_height(self.screen_resolution))
        return self.parent_viewport.x1 + 9 * get_bottom_bar_height(self.screen_resolution) \
            + 6 * bonus_label_window_width // 7

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(22 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return '----'
