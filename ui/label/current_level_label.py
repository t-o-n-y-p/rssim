from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_bottom_bar_height
from ui.label import LocalizedLabel


@final
class CurrentLevelLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.current_level_label'),
            i18n_resources_key='level_string', parent_viewport=parent_viewport
        )
        self.arguments = (0,)
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + 15 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + 3 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return int(22 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
