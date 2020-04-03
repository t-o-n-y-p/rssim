from logging import getLogger

from model import *


class ShopPlaceholderModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, shop_id):
        super().__init__(
            controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.model')
        )
        self.shop_id = shop_id

    def on_save_state(self):
        pass
