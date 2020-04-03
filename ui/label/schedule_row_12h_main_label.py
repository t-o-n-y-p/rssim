from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class ScheduleRow12HMainLabel(LocalizedLabel):
    def __init__(self, column, row, parent_viewport):
        super().__init__(
            logger=getLogger('root.schedule_row_12h_main_label'),
            i18n_resources_key='12h_schedule_row_string', parent_viewport=parent_viewport
        )
        self.arguments = (0, 0, 0, '', 0)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']
        self.column = column
        self.row = row

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) // 5 * 3

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
