from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, localizable_with_resource
from ui.button_v2 import UIButtonV2


@final
class OpenSettingsMainMenuViewButtonV2(UIButtonV2):                                                             # noqa
    @localizable_with_resource('settings_label_string')
    def __init__(self, on_click_action, on_hover_action, on_leave_action, logger, parent_viewport):
        super().__init__(on_click_action, on_hover_action, on_leave_action, logger, parent_viewport)
        self.font_name = 'Perfo'
        self.is_bold = True

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
            - 7 * get_bottom_bar_height(self.screen_resolution) // 2

    def get_y(self):
        return (
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
            + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
        ) // 2 - get_bottom_bar_height(self.screen_resolution) // 2

    def get_width(self):
        return get_bottom_bar_height(self.screen_resolution) * 7

    def get_height(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_font_size(self):
        return int(30 / 80 * get_bottom_bar_height(self.screen_resolution))
