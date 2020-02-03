from logging import getLogger

from controller import *
from model.shop_placeholder_model import ShopPlaceholderModel
from view.shop_placeholder_view import ShopPlaceholderView
from ui.fade_animation.fade_in_animation.shop_placeholder_fade_in_animation import ShopPlaceholderFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_placeholder_fade_out_animation import ShopPlaceholderFadeOutAnimation


class ShopPlaceholderController(MapBaseController):
    def __init__(self, model: ShopPlaceholderModel, view: ShopPlaceholderView, map_id, shop_id, parent_controller):
        super().__init__(model, view, map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.controller'))
        self.shop_id = shop_id
        self.fade_in_animation = ShopPlaceholderFadeInAnimation(self.view)
        self.fade_out_animation = ShopPlaceholderFadeOutAnimation(self.view)

    def create_shop_placeholder_elements(self, shop_id):
        pass
