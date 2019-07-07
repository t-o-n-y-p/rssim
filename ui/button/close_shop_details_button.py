from logging import getLogger

from ui import *
from ui.button import UIButton


class CloseShopDetailsButton(UIButton):
    def __init__(self, on_click_action, parent_viewport):
        super().__init__(logger=getLogger('root.button.close_shop_details_button'), parent_viewport=parent_viewport)
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action

    def get_position(self):
        return (self.parent_viewport.x2 - get_top_bar_height(self.screen_resolution),
                self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution))

    def get_size(self):
        return (get_top_bar_height(self.screen_resolution),
                get_top_bar_height(self.screen_resolution))
