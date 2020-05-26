from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, GROUPS, BATCHES, GREEN_RGB
from ui.label_v2 import LabelV2, argument


@final
class ShopStagePriceLabelV2(LabelV2):
    @argument('price')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_stage_price_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 2

    def get_y(self):
        return self.parent_viewport.y1 + 13 * get_top_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_formatted_text(self):
        return '{0}  ¤'.format(*self.arguments)
