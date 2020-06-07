from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, localizable_with_resource, WHITE_RGB, GREY_RGB
from ui.label_v2 import InteractiveLabelV2


@final
class BonusCodeInteractiveLabelV2(InteractiveLabelV2):                                                          # noqa
    @localizable_with_resource('bonus_code_placeholder_string')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.placeholder_color = GREY_RGB

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
            + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
        ) // 2 + 5 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return get_top_bar_height(self.screen_resolution)
