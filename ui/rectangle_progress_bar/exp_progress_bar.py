from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.current_level_label import CurrentLevelLabel


class ExpProgressBar(RectangleProgressBar):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.exp_progress_bar'), parent_viewport=parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.text_label = CurrentLevelLabel(parent_viewport=self.viewport)

    def get_position(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return (self.parent_viewport.x1 + bottom_bar_height + bottom_bar_height // 8,
                self.parent_viewport.y1 + bottom_bar_height // 8)

    def get_scale(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return bottom_bar_height / 80
