from logging import getLogger

from ui.onboarding_page import OnboardingPage


class ZoomOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.zoom_onboarding_page'))
        self.help_text_key = 'lorem_ipsum_placeholder_string'
