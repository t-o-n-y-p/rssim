from typing import final

from ui import get_bottom_bar_height, get_top_bar_height, WHITE_RGB, localizable_with_resource
from ui.label_v2 import LabelV2


@final
class ShopStorageNotificationCheckboxDescriptionLabelV2(LabelV2):                                               # noqa
    @localizable_with_resource('shop_storage_notification_description_string')
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'left'

    def get_x(self):
        return self.parent_viewport.x1 + 2 * get_bottom_bar_height(self.screen_resolution)

    def get_y(self):
        return self.parent_viewport.y1 + get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5
