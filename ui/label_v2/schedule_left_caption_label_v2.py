from typing import final

from ui import SCHEDULE_ROWS, get_inner_area_rect, get_bottom_bar_height, ORANGE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class ScheduleLeftCaptionLabelV2(LabelV2):                                                                      # noqa
    @localizable_with_resource('schedule_caption_string')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = ORANGE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return self.parent_viewport.x1 + + get_inner_area_rect(self.screen_resolution)[0] \
               + int(6.875 * get_bottom_bar_height(self.screen_resolution)) // 2

    def get_y(self):
        return self.parent_viewport.y1 + get_inner_area_rect(self.screen_resolution)[1] \
               + get_inner_area_rect(self.screen_resolution)[3] \
               - (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3
