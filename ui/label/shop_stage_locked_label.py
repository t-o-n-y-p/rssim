from logging import getLogger

from ui.label import Label
from ui import *


class ShopStageLockedLabel(Label):
    def __init__(self):
        super().__init__(logger=getLogger('root.shop_stage_locked_label'))
        self.text = ''
        self.font_name = 'Webdings'
        self.base_color = GREY_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return int(35 * top_bar_height / 10)

    @staticmethod
    def get_y(screen_resolution):
        top_bar_height = get_top_bar_height(screen_resolution)
        return 14 * top_bar_height // 4

    @staticmethod
    def get_font_size(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return int(24 / 40 * bottom_bar_height)

    def get_formatted_text(self):
        return self.text
