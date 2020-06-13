from typing import final

from pyshaders import from_files_names

from ui import default_object
from ui.label_v2.exp_money_onboarding_label_v2 import ExpMoneyOnboardingLabelV2
from ui.onboarding_page_v2 import OnboardingPageV2


@final
class ExpMoneyOnboardingPageV2(OnboardingPageV2):
    @default_object(ExpMoneyOnboardingLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(
            logger, parent_viewport,
            shader=from_files_names('shaders/shader.vert', 'shaders/onboarding_page/exp_money_onboarding_page.frag')
        )
