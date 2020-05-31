from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, YELLOW_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class UnderConstructionDescriptionLabelV2(LabelV2):                                                             # noqa
    @localizable_with_resource('under_construction_description_string')
    @argument('percentage')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.under_construction_description_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = YELLOW_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(22 * get_bottom_bar_height(self.screen_resolution) / 80)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
