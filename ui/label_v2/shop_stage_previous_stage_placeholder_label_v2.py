from typing import final

from ui import get_bottom_bar_height, GREY_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class ShopStagePreviousStagePlaceholderLabelV2(LabelV2):                                                        # noqa
    @localizable_with_resource('unlock_condition_from_previous_shop_stage_description_string')
    @argument('previous_stage')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREY_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 \
               - get_bottom_bar_height(self.screen_resolution) // 4

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
