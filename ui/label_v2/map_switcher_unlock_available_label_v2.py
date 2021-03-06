from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, GREEN_RGB, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class MapSwitcherUnlockAvailableLabelV2(LabelV2):                                                               # noqa
    @localizable_with_resource('unlock_available_map_switcher_description_string')
    @argument('price')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 + get_top_bar_height(self.screen_resolution)* 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
