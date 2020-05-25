from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, GROUPS, BATCHES, GREEN_RGB
from ui.label_v2 import LabelV2, argument


@final
class MoneyLabelV2(LabelV2):
    @argument('money')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.money_label'), parent_viewport=parent_viewport)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + 15 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + 3 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return int(22 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        money_str = '{0:0>10}  ¤'.format(*self.arguments)
        return ' '.join((money_str[0], money_str[1:4], money_str[4:7], money_str[7:13]))
