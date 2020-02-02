from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class ShopFadeInAnimation(FadeInAnimation):
    def __init__(self, shop_view):
        super().__init__(animation_object=shop_view,
                         logger=getLogger(
                             f'root.app.game.map.{shop_view.map_id}.shop.{shop_view.shop_id}.fade_in_animation'
                         ))
        self.shop_placeholder_fade_in_animation = None
        self.shop_constructor_fade_in_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        if self.animation_object.level >= self.animation_object.level_required:
            self.shop_constructor_fade_in_animation.on_activate()
        else:
            self.shop_placeholder_fade_in_animation.on_activate()
