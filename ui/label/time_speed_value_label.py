from logging import getLogger

from ui.label import LocalizedLabel
from ui import *


@final
class TimeSpeedValueLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.time_speed_value_label'),
                         i18n_resources_key='time_speed_value_string', parent_viewport=parent_viewport)
        self.arguments = (0.0, )
        self.font_name = 'Arial'
        self.base_color = YELLOW_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        circle_radius = 11 * get_bottom_bar_height(self.screen_resolution) / 32
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2 - circle_radius // 8

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 6

    def get_width(self):
        return None

    def get_formatted_text(self):
        if self.arguments[0] < 10:
            return self.text.format(round((self.arguments[0] % 1) * 10), int(self.arguments[0]))

        return f'x{round(self.arguments[0])}'
