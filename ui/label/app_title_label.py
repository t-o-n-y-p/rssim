from logging import getLogger

from ui.label import Label
from ui import *


class AppTitleLabel(Label):
    def __init__(self):
        super().__init__(logger=getLogger('root.app_title_label'))
        self.text = 'Railway Station Simulator'
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 0
        self.base_color = WHITE_RGB
        self.opacity = 0
        self.x = 0
        self.y = 0
        self.anchor_x = 'left'
        self.anchor_y = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return top_bar_height * 2 + top_bar_height // 4

    @staticmethod
    def get_y(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return screen_resolution[1] - top_bar_height // 2

    @staticmethod
    def get_font_size(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return int(16 / 40 * top_bar_height)
