from logging import getLogger
from typing import final

from ui import GREY_RGB, BATCHES, GROUPS, get_bottom_bar_height, get_top_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class MapSwitcherLevelPlaceholderLabelV2(LabelV2):                                                              # noqa
    @localizable_with_resource('unlock_condition_from_level_map_switcher_string')
    @argument('level')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.map_switcher_level_placeholder_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREY_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 - get_top_bar_height(self.screen_resolution)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
