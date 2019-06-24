from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class MainClockLabel12H(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.main_clock_label_12h'),
                         i18n_resources_key='12h_main_clock_string', parent_viewport=parent_viewport)
        self.arguments = (12, 0, 'PM')
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.x2 - int(200 / 80 * bottom_bar_height)

    def get_y(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.y1 + bottom_bar_height // 2

    def get_font_size(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return int(32 / 80 * bottom_bar_height)

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
