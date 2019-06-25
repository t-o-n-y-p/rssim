from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class ShopTitleLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_title_label'),
                         i18n_resources_key='shop_details_title_string', parent_viewport=parent_viewport)
        self.arguments = (0,)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.x1 + top_bar_height // 4

    def get_y(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.y2 - top_bar_height // 2

    def get_font_size(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return int(16 / 40 * top_bar_height)

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)