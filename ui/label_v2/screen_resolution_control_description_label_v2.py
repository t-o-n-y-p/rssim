from logging import getLogger
from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, GROUPS, BATCHES, WHITE_RGB
from ui.label_v2 import LabelV2, localizable_with_resource


@final
class ScreenResolutionControlDescriptionLabelV2(LabelV2):                                                       # noqa
    @localizable_with_resource('windowed_resolution_description_string')
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.screen_resolution_control_description_label'), parent_viewport=parent_viewport
        )
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
