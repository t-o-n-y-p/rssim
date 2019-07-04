from logging import getLogger

from ui.onboarding_page import OnboardingPage
from ui.label.pause_resume_onboarding_label import PauseResumeOnboardingLabel


class PauseResumeOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.pause_resume_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = PauseResumeOnboardingLabel(parent_viewport=self.viewport)
