from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class MapSwitcherUnlockAvailableLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.map_switcher_unlock_available_label'),
            i18n_resources_key='unlock_available_map_switcher_description_string', parent_viewport=parent_viewport
        )
        self.arguments = (0,)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 + get_top_bar_height(self.screen_resolution)* 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments).replace(',', ' ')
