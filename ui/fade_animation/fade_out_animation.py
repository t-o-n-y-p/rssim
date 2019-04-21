from logging import getLogger

from ui.fade_animation import *


class FadeOutAnimation(FadeAnimation):
    def __init__(self, view):
        super().__init__(view=view, logger=getLogger(f'{view.__class__.__name__}.fade_out_animation'))
        self.opacity_chart = [255, 238, 221, 204, 187, 170, 153, 136, 119, 102, 85, 68, 51, 34, 17, 0]

    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_out_animation_deactivate()
