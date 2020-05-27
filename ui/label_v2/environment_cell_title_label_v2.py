from logging import getLogger
from typing import final

from ui import WHITE_RGB, GROUPS, BATCHES, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class EnvironmentCellTitleLabelV2(LabelV2):                                                                     # noqa
    @localizable_with_resource('title_environment_string')
    @argument('tier')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.environment_cell_title_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(0.7 * get_bottom_bar_height(self.screen_resolution))

    def get_font_size(self):
        return int(0.3 * get_bottom_bar_height(self.screen_resolution))
