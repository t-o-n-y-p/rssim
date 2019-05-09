from logging import getLogger

from ui.onboarding_page import OnboardingPage


class SettingsOnboardingPage(OnboardingPage):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.settings_onboarding_page'))
        self.help_text_key = 'settings_onboarding_page_string'
