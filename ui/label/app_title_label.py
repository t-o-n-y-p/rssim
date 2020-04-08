from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_top_bar_height
from ui.label import Label


@final
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
        return self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) * 2 \
               + get_top_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(16 / 40 * get_top_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text
