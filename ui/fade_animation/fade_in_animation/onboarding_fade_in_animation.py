from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class OnboardingFadeInAnimation(FadeInAnimation):
    def __init__(self, onboarding_view):
        super().__init__(animation_object=onboarding_view, logger=getLogger('root.app.onboarding.fade_in_animation'))
