from typing import final

from pyshaders import from_files_names

from ui import default_object
from ui.label_v2.clock_onboarding_label_v2 import ClockOnboardingLabelV2
from ui.onboarding_page_v2 import OnboardingPageV2


@final
class ClockOnboardingPageV2(OnboardingPageV2):
    @default_object(ClockOnboardingLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(
            logger, parent_viewport,
            shader=from_files_names('shaders/shader.vert', 'shaders/onboarding_page/clock_onboarding_page.frag')
        )
