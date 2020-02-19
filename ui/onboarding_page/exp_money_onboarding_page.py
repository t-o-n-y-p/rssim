from logging import getLogger
from typing import final

from ui.onboarding_page import OnboardingPage
from ui.label.exp_money_onboarding_label import ExpMoneyOnboardingLabel


@final
class ExpMoneyOnboardingPage(OnboardingPage):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.exp_money_onboarding_page'),
                         parent_viewport=parent_viewport)
        self.help_label = ExpMoneyOnboardingLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.help_label.on_window_resize)
