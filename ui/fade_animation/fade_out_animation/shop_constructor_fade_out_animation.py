from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class ShopConstructorFadeOutAnimation(FadeOutAnimation):
    def __init__(self, shop_constructor_view):
        super().__init__(animation_object=shop_constructor_view,
                         logger=getLogger(
                             f'root.app.game.map.{shop_constructor_view.map_id}.shop.{shop_constructor_view.shop_id}.constructor.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
