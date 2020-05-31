from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, GREEN_RGB
from ui.label_v2 import LabelV2, argument


@final
class ShopStorageLabelV2(LabelV2):
    @argument('storage_money')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_storage_label'), parent_viewport=parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return self.parent_viewport.x1 + 5 * get_bottom_bar_height(self.screen_resolution) // 2

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(29 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return '{0}  ¤'.format(*self.arguments)
