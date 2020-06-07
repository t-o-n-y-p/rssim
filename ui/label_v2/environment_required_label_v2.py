from typing import final

from ui import GREY_RGB, get_bottom_bar_height, localizable_with_resource
from ui.label_v2 import LabelV2, argument


@final
class EnvironmentRequiredLabelV2(LabelV2):                                                                      # noqa
    @localizable_with_resource('unlock_condition_from_environment_track_description_string')
    @argument('tier')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREY_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(22 * get_bottom_bar_height(self.screen_resolution) / 80)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
