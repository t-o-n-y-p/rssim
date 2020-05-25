from logging import getLogger
from typing import final

from ui import SCHEDULE_ROWS, get_inner_area_rect, GROUPS, BATCHES, WHITE_RGB
from ui.label_v2 import LabelV2, localizable_with_resource, argument


@final
class ScheduleRow24HMainLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('24h_schedule_row_string')
    @argument('train_id')
    @argument('24h_time')
    @argument('cars')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.schedule_row_24h_main_label'), parent_viewport=parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3
