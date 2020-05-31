from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, WHITE_RGB
from ui.label_v2 import LabelV2


@final
class PassengerMapCellIcon1LabelV2(LabelV2):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.passenger_map_cell_icon_1_label'), parent_viewport=parent_viewport)
        self.font_name = 'Webdings'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 + get_top_bar_height(self.screen_resolution)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_formatted_text(self):
        return ''
