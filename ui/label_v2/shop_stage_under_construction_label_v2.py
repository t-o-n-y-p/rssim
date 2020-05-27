from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, GROUPS, BATCHES, YELLOW_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class ShopStageUnderConstructionLabelV2(LabelV2):                                                               # noqa
    @localizable_with_resource('under_construction_shop_stage_description_string')
    @argument('percentage')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_stage_under_construction_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = YELLOW_RGB
        self.anchor_x = 'center'
        self.align = 'center'
        self.multiline = True
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return 4 * get_bottom_bar_height(self.screen_resolution)
