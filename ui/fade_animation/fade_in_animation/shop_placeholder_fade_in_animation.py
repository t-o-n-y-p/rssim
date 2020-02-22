from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class ShopPlaceholderFadeInAnimation(FadeInAnimation):
    def __init__(self, shop_placeholder_view):
        super().__init__(animation_object=shop_placeholder_view,
                         logger=getLogger(
                             f'root.app.game.map.{shop_placeholder_view.map_id}.shop.{shop_placeholder_view.shop_id}.placeholder.fade_in_animation'
                         ))
