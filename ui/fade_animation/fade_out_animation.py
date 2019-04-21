from logging import getLogger

from ui.fade_animation import *


class FadeOutAnimation(FadeAnimation):
    def __init__(self, animation_object):
        super().__init__(animation_object=animation_object,
                         logger=getLogger(f'{animation_object.__class__.__name__}.fade_out_animation'))
        self.opacity_chart = [255, 238, 221, 204, 187, 170, 153, 136, 119, 102, 85, 68, 51, 34, 17, 0]

    @fade_animation_is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_out_animation_deactivate()
