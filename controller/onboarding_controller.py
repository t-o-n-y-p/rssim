from logging import getLogger

from controller import *


@final
class OnboardingController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.onboarding.controller'))

    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.model.on_save_and_commit_onboarding_state()
