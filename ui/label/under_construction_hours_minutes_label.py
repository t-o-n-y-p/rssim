from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class UnderConstructionHoursMinutesLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.under_construction_hours_minutes_label'),
                         i18n_resources_key='under_construction_hours_minutes_description_string',
                         parent_viewport=parent_viewport)
        self.arguments = (0, 0)
        self.font_name = 'Arial'
        self.base_color = YELLOW_RGB
        self.anchor_x = 'left'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x1 + get_bottom_bar_height(self.screen_resolution) // 8

    def get_y(self):
        return self.parent_viewport.y1 + int(22 * get_bottom_bar_height(self.screen_resolution) / 80)

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
