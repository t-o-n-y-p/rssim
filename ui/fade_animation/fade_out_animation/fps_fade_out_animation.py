from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class FPSFadeOutAnimation(FadeOutAnimation):
    def __init__(self, fps_controller):
        super().__init__(animation_object=fps_controller,
                         logger=getLogger('root.app.fps.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
