from logging import getLogger

from ui.onboarding_page import OnboardingPage


class PauseResumeOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.pause_resume_onboarding_page'))
        self.help_text_key = 'pause_resume_onboarding_page_string'
