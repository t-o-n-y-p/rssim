from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class MainClockLabel12H(LocalizedLabel):
    def __init__(self):
        super().__init__(logger=getLogger('root.main_clock_label_12h'),
                         i18n_resources_key='12h_main_clock_string')
        self.args = (12, 0, 'PM')
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return screen_resolution[0] - int(200 / 80 * bottom_bar_height)

    @staticmethod
    def get_y(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return bottom_bar_height // 2

    @staticmethod
    def get_font_size(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return int(32 / 80 * bottom_bar_height)
