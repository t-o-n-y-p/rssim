from logging import getLogger

from pyglet.image import load

from ui.rectangle_progress_bar import RectangleProgressBar
from ui import *
from ui.label.current_level_label import CurrentLevelLabel


@final
class ExpProgressBar(RectangleProgressBar):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.exp_progress_bar'), parent_viewport=parent_viewport)
        self.inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.text_label = CurrentLevelLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.text_label.on_window_resize)

    def get_position(self):
        return (
            self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution)
            + get_bottom_bar_height(self.screen_resolution) // 8,
            self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 8
        )

    def get_scale(self):
        return get_bottom_bar_height(self.screen_resolution) / 80
