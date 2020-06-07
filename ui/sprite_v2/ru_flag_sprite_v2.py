from typing import final

from ui import get_top_bar_height, GROUPS, BATCHES, FLAG_RU
from ui.sprite_v2 import UISpriteV2


@final
class RuFlagSpriteV2(UISpriteV2):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.texture = FLAG_RU
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']
        self.usage = 'static'

    def get_x(self):
        return self.parent_viewport.x1 + get_top_bar_height(self.screen_resolution) // 2 \
            + get_top_bar_height(self.screen_resolution) - 2

    def get_y(self):
        return self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution) // 2

    def get_scale(self):
        return 0.6 * get_top_bar_height(self.screen_resolution) / float(self.texture.width)
