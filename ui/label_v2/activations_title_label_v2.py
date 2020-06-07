from typing import final

from ui import WHITE_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class ActivationsTitleLabelV2(LabelV2):                                                                         # noqa
    @localizable_with_resource('activations_title_label_string')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1

    def get_y(self):
        return self.parent_viewport.y1 + (self.parent_viewport.y2 - self.parent_viewport.y1) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
