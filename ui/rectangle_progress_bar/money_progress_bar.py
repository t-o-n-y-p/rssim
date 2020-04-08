from logging import getLogger
from typing import final

from pyglet.image import load

from ui import get_bottom_bar_height
from ui.rectangle_progress_bar import RectangleProgressBar
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
        return (
            self.parent_viewport.x1 + 5 * get_bottom_bar_height(self.screen_resolution),
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 8
        )

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80
