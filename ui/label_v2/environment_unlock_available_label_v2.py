from logging import getLogger
from typing import final

from ui import GREEN_RGB, BATCHES, GROUPS, get_bottom_bar_height
from ui.label_v2 import LabelV2, localizable_with_resource, argument


@final
class EnvironmentUnlockAvailableLabelV2(LabelV2):                                                               # noqa
    @localizable_with_resource('unlock_available_environment_description_string')
    @argument('price')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.environment_unlock_available_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(22 * get_bottom_bar_height(self.screen_resolution) / 80)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5