from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class SignalFadeOutAnimation(FadeOutAnimation):
    def __init__(self, signal_controller):
        super().__init__(animation_object=signal_controller,
                         logger=getLogger(
                             f'root.app.game.map.{signal_controller.map_id}.signal.{signal_controller.track}.{signal_controller.base_route}.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
