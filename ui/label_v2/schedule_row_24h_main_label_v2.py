from typing import final

from ui import SCHEDULE_ROWS, get_inner_area_rect, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class ScheduleRow24HMainLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('24h_schedule_row_string')
    @argument('train_id')
    @argument('24h_time')
    @argument('cars')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3
