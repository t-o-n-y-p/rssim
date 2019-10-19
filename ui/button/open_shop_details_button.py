from logging import getLogger

from ui import *
from database import CONFIG_DB_CURSOR
from ui.button import MapButton


@final
class OpenShopDetailsButton(MapButton):
    def __init__(self, map_id, shop_id, on_click_action, on_hover_action, on_leave_action):
        super().__init__(logger=getLogger('root.button.open_shop_details_button'))
        self.to_activate_on_controller_init = False
        self.invisible = True
        self.text = ''
        self.font_name = 'Arial'
        self.base_font_size_property = 29 / 80
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action
        CONFIG_DB_CURSOR.execute('''SELECT button_x, button_y FROM shops_config 
                                    WHERE map_id = ? AND shop_id = ?''',
                                 (map_id, shop_id))
        self.shop_button_offset = CONFIG_DB_CURSOR.fetchone()

    def get_position(self):
        return (self.base_offset[0] + self.shop_button_offset[0] // round(1 / self.scale),
                self.base_offset[1] + self.shop_button_offset[1] // round(1 / self.scale))

    def get_size(self):
        return (250 // round(1 / self.scale),
                40 // round(1 / self.scale))
