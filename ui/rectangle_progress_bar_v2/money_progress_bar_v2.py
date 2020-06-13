from typing import final

from pyglet.image import load

from ui import get_bottom_bar_height, default_object
from ui.label_v2.money_label_v2 import MoneyLabelV2
from ui.rectangle_progress_bar_v2 import RectangleProgressBarV2


@final
class MoneyProgressBarV2(RectangleProgressBarV2):
    @default_object(MoneyLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_money_active.png')

    def get_position(self):
        return (
            self.parent_viewport.x1 + 5 * get_bottom_bar_height(self.screen_resolution),
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 8
        )

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80

    def on_money_update(self, money):
        self.money_label_v2.on_money_update(money)                                                              # noqa
