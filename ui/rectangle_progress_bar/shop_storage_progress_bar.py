from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.shop_storage_label import ShopStorageLabel


class ShopStorageProgressBar(RectangleProgressBar):
    def __init__(self):
        super().__init__(logger=getLogger('root.shop_storage_progress_bar'))
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.text_label = ShopStorageLabel()

    @staticmethod
    def get_position(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return int(6.875 * bottom_bar_height) * 2 - bottom_bar_height - 15 * bottom_bar_height // 4, \
               3 * bottom_bar_height + bottom_bar_height // 4
