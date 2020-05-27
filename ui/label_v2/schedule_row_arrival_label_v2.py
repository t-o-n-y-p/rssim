from logging import getLogger
from typing import final

from ui import SCHEDULE_ROWS, get_inner_area_rect, GROUPS, BATCHES, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class ScheduleRowArrivalLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('departed_from_string')
    def __init__(self, map_id, direction, parent_viewport):
        super().__init__(getLogger('root.schedule_row_arrival_label'), parent_viewport, map_id, direction)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
               + 5 * (self.parent_viewport.x2 - self.parent_viewport.x1) // 32

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3
