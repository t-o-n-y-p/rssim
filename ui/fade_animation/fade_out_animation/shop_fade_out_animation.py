from logging import getLogger

from ui.fade_animation.fade_out_animation import *


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
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
        self.shop_placeholder_fade_out_animation.on_activate()
        self.shop_constructor_fade_out_animation.on_activate()
