from logging import getLogger
from typing import final

from ui import get_top_bar_height, GROUPS, BATCHES, FLAG_US
from ui.sprite import UISprite


@final
class USFlagSprite(UISprite):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.view.us_flag_sprite'), parent_viewport=parent_viewport)
        self.texture = FLAG_US
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']
        self.usage = 'static'

    def get_position(self):
        return (
            self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 2,
            self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2
        )

    def get_scale(self):
        return 0.6 * get_top_bar_height(self.screen_resolution) / float(self.texture.width)
