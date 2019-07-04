from logging import getLogger

from ui.onboarding_page import OnboardingPage
from ui.label.zoom_onboarding_label import ZoomOnboardingLabel


class ZoomOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.zoom_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = ZoomOnboardingLabel(parent_viewport=self.viewport)
