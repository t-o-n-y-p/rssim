from logging import getLogger
from typing import final

from ui import get_bottom_bar_height
from ui.button_v2 import UIButtonV2


@final
class SkipOnboardingButtonV2(UIButtonV2):
    def __init__(self, on_click_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.skip_onboarding_button'), parent_viewport=parent_viewport)
        self.font_name = 'Webdings'
        self.on_click_action = on_click_action

    def get_x(self):
        return self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution)

    def get_y(self):
        return self.parent_viewport.y1

    def get_font_size(self):
        return int(40 / 80 * get_bottom_bar_height(self.screen_resolution))

    def get_formatted_text(self):
        return ''

    def get_width(self):
        return get_bottom_bar_height(self.screen_resolution)

    def get_height(self):
        return get_bottom_bar_height(self.screen_resolution)
