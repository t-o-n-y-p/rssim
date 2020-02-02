from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class ConstructorFadeOutAnimation(FadeOutAnimation):
    def __init__(self, constructor_view):
        super().__init__(animation_object=constructor_view,
                         logger=getLogger(
                             f'root.app.game.map.{constructor_view.map_id}.constructor.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
