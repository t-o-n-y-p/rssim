from typing import final

from ui import get_top_bar_height, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class PageControlCounterLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('page_control_label_string')
    @argument('current_page')
    @argument('total_pages')
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
        return int(32 / 80 * get_top_bar_height(self.screen_resolution))
