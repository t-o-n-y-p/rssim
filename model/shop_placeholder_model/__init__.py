from logging import getLogger

from model import *


class ShopPlaceholderModel(MapBaseModel):
    def __init__(self, controller, view, map_id, shop_id):
        super().__init__(controller, view,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.model'))
        self.map_id = map_id
        self.shop_id = shop_id
