from logging import getLogger

from ui.label import LocalizedLabel
from ui import *
from database import PASSENGER_MAP


@final
class PassengerMapCellTitleLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.passenger_map_cell_title_label'),
                         i18n_resources_key='map_title_string',
                         parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 \
               - get_top_bar_height(self.screen_resolution)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text[PASSENGER_MAP]
