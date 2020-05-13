from logging import getLogger
from typing import final

from ui import ORANGE_RGB, BATCHES, GROUPS, get_bottom_bar_height
from ui.label import LocalizedLabel


@final
class ExpBonusValuePercentLabel(LocalizedLabel):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.exp_bonus_value_percent_label'),
            i18n_resources_key='bonus_value_string', parent_viewport=parent_viewport
        )
        self.arguments = (1.0, )
        self.font_name = 'Perfo'
        self.bold = True
        self.base_color = ORANGE_RGB
        self.anchor_x = 'center'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x2 - 6 * get_bottom_bar_height(self.screen_resolution) + 2 \
               - 3 * get_bottom_bar_height(self.screen_resolution) // 16 \
               - int(1.35 * get_bottom_bar_height(self.screen_resolution)) \
               - int(0.675 * get_bottom_bar_height(self.screen_resolution))

    def get_y(self):
        return self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution) // 2

    def get_font_size(self):
        return int(22 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_width(self):
        return None

    def get_formatted_text(self):
        if 1 < self.arguments[0] < 10:
            return self.text.format(
                '{0:0>2}'.format(round(self.arguments[0] * 100) % 100),
                round(self.arguments[0] * 100) // 100
            )
        elif self.arguments[0] < 100:
            return self.text.format(
                round(self.arguments[0] * 10) % 10,
                round(self.arguments[0] * 10) // 10
            )

        return f'x{int(self.arguments[0])}'
