from logging import getLogger

from ui.onboarding_page import OnboardingPage
from ui.label.schedule_onboarding_label import ScheduleOnboardingLabel


class ScheduleOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.schedule_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = ScheduleOnboardingLabel(parent_viewport=self.viewport)
