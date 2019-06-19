from logging import getLogger

from ui.onboarding_page import OnboardingPage


class ConstructorOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.constructor_onboarding_page'))
        self.help_text_key = 'constructor_onboarding_page_string'