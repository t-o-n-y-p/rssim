from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class FPSFadeInAnimation(FadeInAnimation):
    def __init__(self, fps_view):
        super().__init__(animation_object=fps_view, logger=getLogger('root.app.fps.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
