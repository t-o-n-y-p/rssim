from logging import getLogger

from ui.fade_animation import *


class FadeInAnimation(FadeAnimation):
    def __init__(self, view):
        super().__init__(view=view, logger=getLogger(f'{view.__class__.__name__}.fade_in_animation'))
        self.opacity_chart = [0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187, 204, 221, 238, 255]

    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_in_animation_deactivate()
