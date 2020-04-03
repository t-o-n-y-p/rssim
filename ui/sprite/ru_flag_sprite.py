from logging import getLogger

from ui import *
from ui.sprite import UISprite
from textures import FLAG_RU


@final
class RUFlagSprite(UISprite):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.view.ru_flag_sprite'), parent_viewport=parent_viewport)
        self.texture = FLAG_RU
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']
        self.usage = 'static'

    def get_position(self):
        return (
            self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 2
            + get_top_bar_height(self.screen_resolution) - 2,
            self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2
        )

    def get_scale(self):
        return 0.6 * get_top_bar_height(self.screen_resolution) / float(self.texture.width)
