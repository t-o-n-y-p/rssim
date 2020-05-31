from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR
from ui import SHOP_DETAILS_BUTTON_NORMAL_SIZE, MAP_CAMERA
from ui.button_v2 import MapButtonV2


@final
class OpenShopDetailsButtonV2(MapButtonV2):
    def __init__(self, map_id, shop_id, on_click_action, on_hover_action, on_leave_action):
        super().__init__(logger=getLogger('root.button.open_shop_details_button'))
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action
        CONFIG_DB_CURSOR.execute(
            '''SELECT button_x, button_y FROM shops_config WHERE map_id = ? AND shop_id = ?''', (map_id, shop_id)
        )
        self.x, self.y = CONFIG_DB_CURSOR.fetchone()

    def get_width(self):
        return int(MAP_CAMERA.zoom * SHOP_DETAILS_BUTTON_NORMAL_SIZE[0])

    def get_height(self):
        return int(MAP_CAMERA.zoom * SHOP_DETAILS_BUTTON_NORMAL_SIZE[1])
