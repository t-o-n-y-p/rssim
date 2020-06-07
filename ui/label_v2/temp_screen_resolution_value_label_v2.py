from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, WHITE_RGB
from ui.label_v2 import LabelV2, argument


@final
class TempScreenResolutionValueLabelV2(LabelV2):
    @argument('screen_resolution')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return self.parent_viewport.y1 + get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_formatted_text(self):
        return '{0}x{1}'.format(*self.arguments)
