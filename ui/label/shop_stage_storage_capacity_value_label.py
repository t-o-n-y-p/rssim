from logging import getLogger

from ui.label import Label
from ui import *


@final
class ShopStageStorageCapacityValueLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.shop_stage_storage_capacity_value_label'), parent_viewport=parent_viewport
        )
        self.text = '{0}  ¤'
        self.arguments = (0, )
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x2 - get_top_bar_height(self.screen_resolution) * 3

    def get_y(self):
        return self.parent_viewport.y2 - 13 * get_top_bar_height(self.screen_resolution) // 8 \
               - 4 * get_top_bar_height(self.screen_resolution) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        money_str = self.text.format(*self.arguments)
        if len(money_str) < 7:
            return money_str

        return ' '.join((money_str[0:len(money_str) - 6], money_str[len(money_str) - 6:len(money_str)]))
