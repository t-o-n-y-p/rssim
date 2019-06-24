from logging import getLogger

from ui.label import Label
from ui import *


class MoneyLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.money_label'), parent_viewport=parent_viewport)
        self.text = '{0:0>10}  ¤'
        self.arguments = (0, )
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.x1 + 15 * bottom_bar_height // 8

    def get_y(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.y1 + 3 * bottom_bar_height // 8

    def get_font_size(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return int(22 / 80 * bottom_bar_height)

    def get_width(self):
        return None

    def get_formatted_text(self):
        money_str = self.text.format(*self.arguments)
        return ' '.join((money_str[0], money_str[1:4], money_str[4:7], money_str[7:13]))
