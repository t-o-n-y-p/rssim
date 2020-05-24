from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_top_bar_height, get_bottom_bar_height
from ui.label_v2 import LabelV2, localizable_with_resource


@final
class MapCellTitleLabelV2(LabelV2):                                                                             # noqa
    @localizable_with_resource('map_title_string')
    def __init__(self, map_id, parent_viewport):
        super().__init__(getLogger(f'root.map_cell_title_label.{map_id}'), parent_viewport, map_id)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 - get_top_bar_height(self.screen_resolution)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
