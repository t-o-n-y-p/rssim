from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.money_label import MoneyLabel


@final
class MoneyProgressBar(RectangleProgressBar):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.money_progress_bar'), parent_viewport=parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.text_label = MoneyLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.text_label.on_window_resize)

    def get_position(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return (self.parent_viewport.x1 + 5 * bottom_bar_height,
                self.parent_viewport.y1 + bottom_bar_height // 8)

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80
