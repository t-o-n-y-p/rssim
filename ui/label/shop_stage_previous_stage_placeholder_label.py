from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class ShopStagePreviousStagePlaceholderLabel(LocalizedLabel):
    def __init__(self, viewport):
        super().__init__(logger=getLogger('root.shop_stage_level_placeholder_label'),
                         i18n_resources_key='unlock_condition_from_previous_shop_stage_description_string',
                         viewport=viewport)
        self.arguments = (0,)
        self.font_name = 'Arial'
        self.base_color = GREY_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.viewport.x1 + self.viewport.x2) // 2

    def get_y(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return (self.viewport.y1 + self.viewport.y2) // 2 - bottom_bar_height // 4

    def get_font_size(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return bottom_bar_height // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
