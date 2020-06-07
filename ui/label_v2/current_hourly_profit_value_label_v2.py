from typing import final

from ui import GREEN_RGB, get_bottom_bar_height
from ui.label_v2 import LabelV2, argument


@final
class CurrentHourlyProfitValueLabelV2(LabelV2):
    @argument('hourly_profit')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8 + \
               4 * get_bottom_bar_height(self.screen_resolution)

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 8 \
               + 3 * get_bottom_bar_height(self.screen_resolution) \
               + 2 * get_bottom_bar_height(self.screen_resolution) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_formatted_text(self):
        return '{0}  ¤'.format(*self.arguments)
