from logging import getLogger
from typing import final

from ui import is_not_active, is_active


@final
class TransitionAnimation:
    def __init__(self, fade_out_animation, fade_in_animation):
        self.logger = getLogger(
            'root.{}->{}_transition_animation'.format(
                fade_out_animation.animation_object.__class__.__name__,
                fade_in_animation.animation_object.__class__.__name__
            )
        )
        self.fade_out_animation, self.fade_in_animation = fade_out_animation, fade_in_animation
        self.is_activated = False

    @is_not_active
    def on_activate(self):
        self.is_activated = True
        self.fade_out_animation.on_activate()
        self.fade_out_animation.on_deactivate_listener = self
        self.fade_in_animation.on_deactivate_listener = self

    @is_active
    def on_deactivate(self):
        self.is_activated = False
        self.fade_out_animation.on_deactivate()
        self.fade_in_animation.on_deactivate()
        self.fade_out_animation.on_deactivate_listener = None
        self.fade_in_animation.on_deactivate_listener = None

    def on_fade_out_animation_deactivate(self):
        self.fade_in_animation.on_activate()

    def on_fade_in_animation_deactivate(self):
        self.on_deactivate()
