from logging import getLogger

from ui.label import Label
from ui import *


class FPSLabel(Label):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.fps_label'), parent_viewport=parent_viewport)
        self.text = '{0} FPS'
        self.arguments = (0, )
        self.font_name = 'Courier New'
        self.base_color = WHITE_RGB
        self.anchor_x = 'right'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        top_bar_height = get_top_bar_height(self.screen_resolution)
        return self.parent_viewport.x2 - top_bar_height * 3 - top_bar_height // 4

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
