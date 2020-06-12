from typing import final

from ui import SCHEDULE_ROWS, get_inner_area_rect, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, resource_list_key


@final
class ScheduleRowArrivalLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('departed_from_string')
    @resource_list_key('map_id')
    @resource_list_key('direction')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
            + 5 * (self.parent_viewport.x2 - self.parent_viewport.x1) // 32

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3
