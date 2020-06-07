from typing import final

from ui import ORANGE_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class BonusInfoCellExpBonusValueLabelV2(LabelV2):                                                               # noqa
    @localizable_with_resource('exp_bonus_value_label_string')
    @argument('bonus_value')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = ORANGE_RGB
        self.anchor_x = 'right'

    def get_x(self):
        return self.parent_viewport.x2

    def get_y(self):
        return self.parent_viewport.y1 + 2 * (self.parent_viewport.y2 - self.parent_viewport.y1) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
