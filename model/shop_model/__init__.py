from abc import ABC
from logging import getLogger

from database import CONFIG_DB_CURSOR
from model import MapBaseModel


class ShopModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, shop_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.shop_id = shop_id
        CONFIG_DB_CURSOR.execute(
            '''SELECT level_required FROM shops_config WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id)
        )
        self.level_required = CONFIG_DB_CURSOR.fetchone()[0]

    def on_save_state(self):
        pass
