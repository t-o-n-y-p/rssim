from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.money_label import MoneyLabel


class MoneyProgressBar(RectangleProgressBar):
    def __init__(self):
        super().__init__(logger=getLogger('root.money_progress_bar'))
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.text_label = MoneyLabel()

    @staticmethod
    def get_position(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return 5 * bottom_bar_height, bottom_bar_height // 8
