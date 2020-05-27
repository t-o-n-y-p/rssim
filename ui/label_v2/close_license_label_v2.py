from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class CloseLicenseLabelV2(LabelV2):                                                                             # noqa
    @localizable_with_resource('back_to_the_main_menu_placeholder_string')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.close_license_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + 5 * get_bottom_bar_height(self.screen_resolution) // 4

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
