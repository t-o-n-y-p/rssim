from logging import getLogger

from ui.label import Label
from ui import *


class ShopStorageLabel(Label):
    def __init__(self):
        super().__init__(logger=getLogger('root.shop_storage_label'))
        self.text = '{0}  ¤'
        self.arguments = (0, )
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @staticmethod
    def get_x(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return 5 * bottom_bar_height // 2

    @staticmethod
    def get_y(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return bottom_bar_height // 2

    @staticmethod
    def get_font_size(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return int(29 / 80 * bottom_bar_height)

    def get_formatted_text(self):
        money_str = self.text.format(*self.arguments)
        if len(money_str) < 7:
            return money_str
        else:
            return ' '.join((money_str[0:len(money_str) - 6], money_str[len(money_str) - 6:len(money_str)]))
