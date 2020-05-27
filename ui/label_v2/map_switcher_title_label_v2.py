from logging import getLogger
from typing import final

from ui import get_top_bar_height, GROUPS, BATCHES, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class MapSwitcherTitleLabelV2(LabelV2):                                                                         # noqa
    @localizable_with_resource('map_switcher_title_string')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.map_switcher_title_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(16 / 40 * get_top_bar_height(self.screen_resolution))
