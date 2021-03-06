from typing import final

from ui import WHITE_RGB, get_bottom_bar_height
from ui.label_v2 import LabelV2, argument


@final
class ActivationsValueLabelV2(LabelV2):
    @argument('activations_left')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'right'

    def get_x(self):
        return self.parent_viewport.x2

    def get_y(self):
        return self.parent_viewport.y1 + (self.parent_viewport.y2 - self.parent_viewport.y1) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_formatted_text(self):
        return '{0}'.format(*self.arguments)
