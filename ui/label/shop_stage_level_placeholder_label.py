from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class ShopStageLevelPlaceholderLabel(LocalizedLabel):
    def __init__(self):
        super().__init__(logger=getLogger('root.shop_stage_level_placeholder_label'),
                         i18n_resources_key='unlock_condition_from_level_shop_stage_string')
        self.arguments = (0,)
        self.font_name = 'Arial'
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
        return 9 * top_bar_height // 4

    @staticmethod
    def get_font_size(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return bottom_bar_height // 5

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
