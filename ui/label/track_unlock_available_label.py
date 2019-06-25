from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


class TrackUnlockAvailableLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.track_unlock_available_label'),
                         i18n_resources_key='unlock_available_track_description_string',
                         parent_viewport=parent_viewport)
        self.arguments = (0,)
        self.font_name = 'Arial'
        self.base_color = GREEN_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.x1 + bottom_bar_height // 8

    def get_y(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return self.parent_viewport.y1 + int(22 * bottom_bar_height / 80)

    def get_font_size(self):
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        return bottom_bar_height // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments).replace(',', ' ')