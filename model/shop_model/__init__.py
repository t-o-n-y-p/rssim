from logging import getLogger

from model import *


class ShopModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('SELECT level FROM game_progress')
        self.level = self.user_db_cursor.fetchone()[0]
        self.config_db_cursor.execute('''SELECT level_required FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = self.config_db_cursor.fetchone()[0]

    def on_activate_view(self):
        self.view.on_activate()

    def on_level_up(self, level):
        self.level = level
