from logging import getLogger

from ui import *
from ui.button import UIButton


class OpenScheduleButton(UIButton):
    def __init__(self, on_click_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.open_schedule_button'), parent_viewport=parent_viewport)
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 32 / 80
        self.on_click_action = on_click_action

    def get_position(self):
        return (self.parent_viewport.x2 - 6 * get_bottom_bar_height(self.screen_resolution) + 2,
                self.parent_viewport.y1)

    def get_size(self):
        return (get_bottom_bar_height(self.screen_resolution),
                get_bottom_bar_height(self.screen_resolution))
