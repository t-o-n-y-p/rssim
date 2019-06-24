from logging import getLogger

from ui.label import Label
from ui import *


class AppTitleLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app_title_label'), parent_viewport=parent_viewport)
        self.text = 'Railway Station Simulator'
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.x1 + top_bar_height * 2 + top_bar_height // 4

    def get_y(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.y2 - top_bar_height // 2

    def get_font_size(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return int(16 / 40 * top_bar_height)

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text
