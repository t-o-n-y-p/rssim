from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class MainClockLabel24HV2(LabelV2):                                                                             # noqa
    @localizable_with_resource('24h_main_clock_string')
    @argument('24h_time')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.main_clock_label_24h'), parent_viewport=parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x2 - int(280 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(32 / 80 * get_bottom_bar_height(self.screen_resolution))
