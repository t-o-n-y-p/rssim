from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.current_level_label import CurrentLevelLabel


class ExpProgressBar(RectangleProgressBar):
    def __init__(self):
        super().__init__(logger=getLogger('root.exp_progress_bar'))
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.text_label = CurrentLevelLabel()

    @staticmethod
    def get_position(screen_resolution):
        bottom_bar_height = get_bottom_bar_height(screen_resolution)
        return bottom_bar_height + bottom_bar_height // 8, bottom_bar_height // 8
