from logging import getLogger

from ui.label import Label
from ui import *


class FPSLabel(Label):
    def __init__(self, args):
        super().__init__(logger=getLogger('root.fps_label'), args=args)
        self.text = '{0} FPS'
        self.font_name = 'Courier New'
        self.base_color = WHITE_RGB
        self.anchor_x = 'right'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return screen_resolution[0] - top_bar_height * 3 - top_bar_height // 4

    @staticmethod
    def get_y(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return screen_resolution[1] - top_bar_height // 2

    @staticmethod
    def get_font_size(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return int(16 / 40 * top_bar_height)
