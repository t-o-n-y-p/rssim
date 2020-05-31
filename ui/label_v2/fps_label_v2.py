from logging import getLogger
from typing import final

from ui import WHITE_RGB, get_top_bar_height
from ui.label_v2 import LabelV2, argument


@final
class FPSLabelV2(LabelV2):
    @argument('fps')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.fps_label'), parent_viewport=parent_viewport)
        self.font_name = 'Courier New'
        self.base_color = WHITE_RGB
        self.anchor_x = 'right'

    def get_x(self):
        return self.parent_viewport.x2 - get_top_bar_height(self.screen_resolution) * 3 \
               - get_top_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(16 / 40 * get_top_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return '{0} FPS'.format(*self.arguments)
