from logging import getLogger

from model import *


class ShopPlaceholderModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.model'))
        self.map_id = map_id
        self.shop_id = shop_id

    def on_activate_view(self):
        self.view.on_activate()
