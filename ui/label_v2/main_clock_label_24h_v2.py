from typing import final

from ui import WHITE_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class MainClockLabel24HV2(LabelV2):                                                                             # noqa
    @localizable_with_resource('24h_main_clock_string')
    @argument('24h_time')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return self.parent_viewport.x2 - int(280 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(32 / 80 * get_bottom_bar_height(self.screen_resolution))
