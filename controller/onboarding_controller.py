from logging import getLogger
from typing import final

from controller import AppBaseController
from model.onboarding_model import OnboardingModel
from view.onboarding_view import OnboardingView
from ui.fade_animation.fade_in_animation.onboarding_fade_in_animation import OnboardingFadeInAnimation
from ui.fade_animation.fade_out_animation.onboarding_fade_out_animation import OnboardingFadeOutAnimation


@final
class OnboardingController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.onboarding.controller'))
        self.view = OnboardingView(controller=self)
        self.model = OnboardingModel(controller=self, view=self.view)
        self.fade_in_animation = OnboardingFadeInAnimation(self.view)
        self.fade_out_animation = OnboardingFadeOutAnimation(self.view)

    def on_save_and_commit_onboarding_state(self):
        self.model.on_save_and_commit_onboarding_state()
