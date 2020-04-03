from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.shop_placeholder_fade_in_animation import ShopPlaceholderFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_placeholder_fade_out_animation import ShopPlaceholderFadeOutAnimation


class ShopPlaceholderController(MapBaseController, ABC):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(
            map_id, parent_controller,
            logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.controller')
        )
        self.view, self.model = self.create_view_and_model(shop_id)
        self.shop_id = shop_id
        self.fade_in_animation = ShopPlaceholderFadeInAnimation(self.view)
        self.fade_out_animation = ShopPlaceholderFadeOutAnimation(self.view)
