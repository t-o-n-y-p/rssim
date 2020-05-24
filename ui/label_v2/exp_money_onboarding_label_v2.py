from logging import getLogger
from typing import final

from ui import WHITE_RGB, BATCHES, GROUPS, get_bottom_bar_height
from ui.label_v2 import LabelV2, localizable_with_resource


@final
class ExpMoneyOnboardingLabelV2(LabelV2):                                                                       # noqa
    @localizable_with_resource('exp_money_onboarding_page_string')
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.exp_money_onboarding_label'), parent_viewport=parent_viewport)
        self.font_name = 'Arial'
        self.base_color = WHITE_RGB
        self.anchor_x = 'center'
        self.align = 'center'
        self.multiline = True
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return self.parent_viewport.x2 - (self.parent_viewport.x2 - self.parent_viewport.x1) // 4

    def get_y(self):
        return (self.parent_viewport.y1 + self.parent_viewport.y2) // 2

    def get_font_size(self):
        return get_bottom_bar_height(self.screen_resolution) // 5

    def get_width(self):
        return 7 * (self.parent_viewport.x2 - self.parent_viewport.x1) // 16
