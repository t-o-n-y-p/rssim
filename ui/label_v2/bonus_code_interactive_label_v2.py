from logging import getLogger
from typing import final

from ui import BATCHES, GROUPS, get_bottom_bar_height, get_top_bar_height
from ui.label_v2 import InteractiveLabelV2, localizable_with_resource


@final
class BonusCodeInteractiveLabelV2(InteractiveLabelV2):                                                          # noqa
    @localizable_with_resource('bonus_code_placeholder_string')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.bonus_code_interactive_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
            + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
        ) // 2 + 5 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return get_top_bar_height(self.screen_resolution)

    def get_width(self):
        return None
