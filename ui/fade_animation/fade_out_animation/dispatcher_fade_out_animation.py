from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class DispatcherFadeOutAnimation(FadeOutAnimation):
    def __init__(self, dispatcher_controller):
        super().__init__(animation_object=dispatcher_controller,
                         logger=getLogger(
                             f'root.app.game.map.{dispatcher_controller.map_id}.dispatcher.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
