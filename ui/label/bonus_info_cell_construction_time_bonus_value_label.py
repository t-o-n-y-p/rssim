from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class BonusInfoCellConstructionTimeBonusValueLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.construction_time_bonus_value_label'),
            i18n_resources_key='construction_time_bonus_value_label_string', parent_viewport=parent_viewport
        )
        self.arguments = (0, )
        self.font_name = 'Arial'
        self.base_color = YELLOW_RGB
        self.anchor_x = 'right'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x2

    def get_y(self):
        return self.parent_viewport.y1 + 2 * (self.parent_viewport.y2 - self.parent_viewport.y1) // 3

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
