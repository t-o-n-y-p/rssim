from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class ShopModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        USER_DB_CURSOR.execute('SELECT level FROM game_progress')
        self.level = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute('''SELECT level_required FROM shops_config
                                    WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = CONFIG_DB_CURSOR.fetchone()[0]

    def on_activate_view(self):
        self.view.on_activate()

    def on_level_up(self, level):
        self.level = level
