from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class ShopFadeOutAnimation(FadeOutAnimation):
    def __init__(self, shop_controller):
        super().__init__(animation_object=shop_controller,
                         logger=getLogger(
                             f'root.app.game.map.{shop_controller.map_id}.shop.{shop_controller.shop_id}.fade_out_animation'
                         ))
        self.shop_placeholder_fade_out_animation = None
        self.shop_constructor_fade_out_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shop_placeholder_fade_out_animation.on_activate()
        self.shop_constructor_fade_out_animation.on_activate()
