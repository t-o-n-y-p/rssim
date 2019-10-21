from logging import getLogger

from controller import *


class ShopPlaceholderController(GameBaseController):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.controller'))
        self.map_id = map_id
        self.shop_id = shop_id
