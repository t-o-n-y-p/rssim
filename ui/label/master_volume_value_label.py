from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, GROUPS, BATCHES, WHITE_RGB
from ui.label import Label


@final
class MasterVolumeValueLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.master_volume_value_label'), parent_viewport=parent_viewport)
        self.arguments = (0, )
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        circle_radius = 11 * get_bottom_bar_height(self.screen_resolution) / 32
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 - circle_radius // 8

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 6

    def get_width(self):
        return None

    def get_formatted_text(self):
        return str(self.arguments[0])
