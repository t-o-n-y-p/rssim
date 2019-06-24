from logging import getLogger

from ui.label import Label
from ui import *


class ShopLockedLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_locked_label'), parent_viewport=parent_viewport)
        self.text = ''
        self.font_name = 'Webdings'
        self.base_color = GREY_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return (self.parent_viewport.y1 + self.parent_viewport.y2 - top_bar_height) // 2 + top_bar_height

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text
