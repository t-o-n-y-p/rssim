from logging import getLogger

from ui.onboarding_page import OnboardingPage


class BottomBarOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.bottom_bar__onboarding_page'))
        self.help_text_key = 'lorem_ipsum_placeholder_string'
