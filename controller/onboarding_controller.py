from logging import getLogger

from controller import *
from model.onboarding_model import OnboardingModel
from view.onboarding_view import OnboardingView
from ui.fade_animation.fade_in_animation.onboarding_fade_in_animation import OnboardingFadeInAnimation
from ui.fade_animation.fade_out_animation.onboarding_fade_out_animation import OnboardingFadeOutAnimation


@final
class OnboardingController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.onboarding.controller'))
        self.fade_in_animation = OnboardingFadeInAnimation(self)
        self.fade_out_animation = OnboardingFadeOutAnimation(self)
        self.view = OnboardingView(controller=self)
        self.model = OnboardingModel(controller=self, view=self.view)
        self.view.on_init_content()

    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.model.on_save_and_commit_onboarding_state()
