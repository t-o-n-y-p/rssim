from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class PageControlCounterLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.page_control_counter_label'),
                         i18n_resources_key='page_control_label_string',
                         parent_viewport=parent_viewport)
        self.arguments = (0, 0)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return self.parent_viewport.y1 + get_top_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(32 / 80 * get_top_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        return self.text.format(*self.arguments)
