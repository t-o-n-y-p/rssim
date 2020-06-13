from typing import final

from pyshaders import from_files_names

from ui import default_object
from ui.label_v2.schedule_onboarding_label_v2 import ScheduleOnboardingLabelV2
from ui.onboarding_page_v2 import OnboardingPageV2


@final
class ScheduleOnboardingPageV2(OnboardingPageV2):
    @default_object(ScheduleOnboardingLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(
            logger, parent_viewport,
            shader=from_files_names('shaders/shader.vert', 'shaders/onboarding_page/schedule_onboarding_page.frag')
        )
