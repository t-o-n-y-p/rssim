from logging import getLogger
from typing import final

from ui.onboarding_page import OnboardingPage
from ui.label.constructor_onboarding_label import ConstructorOnboardingLabel


@final
class ConstructorOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.constructor_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = ConstructorOnboardingLabel(parent_viewport=self.viewport)
        self.on_resize_handlers.append(self.help_label.on_resize)
