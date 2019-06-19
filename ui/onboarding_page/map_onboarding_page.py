from logging import getLogger

from ui.onboarding_page import OnboardingPage


class MapOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.map_onboarding_page'))
        self.help_text_key = 'map_onboarding_page_string'