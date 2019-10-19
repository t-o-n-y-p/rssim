from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class OnboardingFadeOutAnimation(FadeOutAnimation):
    def __init__(self, onboarding_controller):
        super().__init__(animation_object=onboarding_controller,
                         logger=getLogger('root.app.onboarding.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
