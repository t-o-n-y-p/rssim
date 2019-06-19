from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class ShopPlaceholderFadeInAnimation(FadeInAnimation):
    def __init__(self, shop_controller):
        super().__init__(animation_object=shop_controller,
                         logger=getLogger(
                             f'root.app.game.map.{shop_controller.map_id}.shop.{shop_controller.shop_id}.placeholder.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()