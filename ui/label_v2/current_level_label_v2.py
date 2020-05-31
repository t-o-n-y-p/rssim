from logging import getLogger
from typing import final

from ui import WHITE_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class CurrentLevelLabelV2(LabelV2):                                                                             # noqa
    @localizable_with_resource('level_string')
    @argument('level')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.current_level_label'), parent_viewport=parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return self.parent_viewport.x1 + 15 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + 3 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return int(22 / 80 * get_bottom_bar_height(self.screen_resolution))
