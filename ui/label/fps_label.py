from logging import getLogger

from ui.label import Label
from ui import *


@final
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
        return self.parent_viewport.x2 - get_top_bar_height(self.screen_resolution) * 3 \
               - get_top_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(16 / 40 * get_top_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
