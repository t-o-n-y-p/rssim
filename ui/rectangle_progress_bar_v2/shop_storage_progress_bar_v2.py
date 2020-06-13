from typing import final

from pyglet.image import load

from ui import get_bottom_bar_height, default_object
from ui.label_v2.shop_storage_label_v2 import ShopStorageLabelV2
from ui.rectangle_progress_bar_v2 import RectangleProgressBarV2


@final
class ShopStorageProgressBarV2(RectangleProgressBarV2):
    @default_object(ShopStorageLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')

    def get_position(self):
        return (
            self.parent_viewport.x1 + int(6.875 * get_bottom_bar_height(self.screen_resolution)) * 2
            - get_bottom_bar_height(self.screen_resolution) - 5 * get_bottom_bar_height(self.screen_resolution),
            self.parent_viewport.y1 + 3 * get_bottom_bar_height(self.screen_resolution)
            + get_bottom_bar_height(self.screen_resolution) // 8
        )

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80 * (4/3)

    def on_storage_money_update(self, storage_money):
        self.shop_storage_label_v2.on_storage_money_update(storage_money)                                       # noqa
