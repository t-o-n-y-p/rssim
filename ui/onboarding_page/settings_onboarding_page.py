from logging import getLogger
from typing import final

from ui.onboarding_page import OnboardingPage
from ui.label.settings_onboarding_label import SettingsOnboardingLabel


@final
class SettingsOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.settings_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = SettingsOnboardingLabel(parent_viewport=self.viewport)
