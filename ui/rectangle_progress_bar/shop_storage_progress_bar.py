from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.shop_storage_label import ShopStorageLabel


@final
class ShopStorageProgressBar(RectangleProgressBar):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.shop_storage_progress_bar'), parent_viewport=parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.text_label = ShopStorageLabel(parent_viewport=self.viewport)
        self.on_resize_handlers.append(self.text_label.on_resize)

    def get_position(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return (self.parent_viewport.x1 + int(6.875 * bottom_bar_height) * 2
                - bottom_bar_height - 5 * bottom_bar_height,
                self.parent_viewport.y1 + 3 * bottom_bar_height + bottom_bar_height // 8)

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80 * (4/3)
