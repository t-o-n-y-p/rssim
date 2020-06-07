from typing import final

from ui import get_top_bar_height, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class ShopTitleLabelV2(LabelV2):                                                                                # noqa
    @localizable_with_resource('shop_details_title_string')
    @argument('shop_id')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(16 / 40 * get_top_bar_height(self.screen_resolution))
