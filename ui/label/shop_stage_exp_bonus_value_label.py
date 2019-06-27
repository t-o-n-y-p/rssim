from logging import getLogger
from math import modf

from ui.label import LocalizedLabel
from ui import *


class ShopStageExpBonusValueLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_stage_exp_bonus_value_label'),
                         i18n_resources_key='exp_bonus_value_string', parent_viewport=parent_viewport)
        self.arguments = (0.0, )
        self.font_name = 'Arial'
        self.base_color = ORANGE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.x2 - top_bar_height * 2

    def get_y(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.y2 - 13 * top_bar_height // 8 - 2 * top_bar_height // 3

    def get_font_size(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return bottom_bar_height // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*modf(*self.arguments))
