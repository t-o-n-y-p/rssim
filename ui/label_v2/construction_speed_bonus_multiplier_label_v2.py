from logging import getLogger
from typing import final

from ui import BATCHES, GROUPS, get_bottom_bar_height, YELLOW_RGB
from ui.label_v2 import MultiplierLabelV2


@final
class ConstructionSpeedBonusMultiplierLabelV2(MultiplierLabelV2):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.construction_speed_bonus_value_percent_label'), parent_viewport=parent_viewport,
            precise_index=2
        )
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = YELLOW_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

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
