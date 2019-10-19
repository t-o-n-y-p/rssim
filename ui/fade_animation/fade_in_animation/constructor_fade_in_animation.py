from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class ConstructorFadeInAnimation(FadeInAnimation):
    def __init__(self, constructor_controller):
        super().__init__(animation_object=constructor_controller,
                         logger=getLogger(
                             f'root.app.game.map.{constructor_controller.map_id}.constructor.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
