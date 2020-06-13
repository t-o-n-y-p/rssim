from typing import final

from pyshaders import from_files_names

from ui import default_object
from ui.label_v2.constructor_onboarding_label_v2 import ConstructorOnboardingLabelV2
from ui.onboarding_page_v2 import OnboardingPageV2


@final
class ConstructorOnboardingPageV2(OnboardingPageV2):
    @default_object(ConstructorOnboardingLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(
            logger, parent_viewport,
            shader=from_files_names('shaders/shader.vert', 'shaders/onboarding_page/constructor_onboarding_page.frag')
        )
