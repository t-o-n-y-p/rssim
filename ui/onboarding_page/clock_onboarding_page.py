from logging import getLogger
from typing import final

from ui.onboarding_page import OnboardingPage
from ui.label.clock_onboarding_label import ClockOnboardingLabel


@final
class ClockOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.app.onboarding.clock_onboarding_page'), parent_viewport=parent_viewport
        )
        self.help_label = ClockOnboardingLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.help_label.on_window_resize)
