from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class CurrentLevelLabel(LocalizedLabel):
    def __init__(self):
        super().__init__(logger=getLogger('root.current_level_label'),
                         i18n_resources_key='level_string')
        self.arguments = (0,)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return 15 * bottom_bar_height // 8

    @staticmethod
    def get_y(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return 3 * bottom_bar_height // 8

    @staticmethod
    def get_font_size(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return int(22 / 80 * bottom_bar_height)

    @staticmethod
    def get_width(screen_resolution):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
