from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_bottom_bar_height
from ui.label_v2 import LabelV2, localizable_with_resource


@final
class CurrentExpBonusDescriptionLabelV2(LabelV2):                                                               # noqa
    @localizable_with_resource('current_exp_bonus_string')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.current_exp_bonus_description_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 8 \
               + 3 * get_bottom_bar_height(self.screen_resolution) + get_bottom_bar_height(self.screen_resolution) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5