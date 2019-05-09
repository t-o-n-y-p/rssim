from logging import getLogger

from ui.onboarding_page import OnboardingPage


class ScheduleOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.schedule_onboarding_page'))
        self.help_text_key = 'lorem_ipsum_placeholder_string'
