from typing import final

from ui import WHITE_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class EnvironmentCellTitleLabelV2(LabelV2):                                                                     # noqa
    @localizable_with_resource('title_environment_string')
    @argument('tier')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(0.7 * get_bottom_bar_height(self.screen_resolution))

    def get_font_size(self):
        return int(0.3 * get_bottom_bar_height(self.screen_resolution))
