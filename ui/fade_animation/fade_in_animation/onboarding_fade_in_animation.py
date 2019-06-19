from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class OnboardingFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Onboarding view.
    """
    def __init__(self, onboarding_controller):
        """
        :param onboarding_controller:           Onboarding controller
        """
        super().__init__(animation_object=onboarding_controller,
                         logger=getLogger('root.app.onboarding.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()