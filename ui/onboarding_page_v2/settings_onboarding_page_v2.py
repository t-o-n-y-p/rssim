from typing import final

from pyshaders import from_files_names

from ui import default_object
from ui.label_v2.settings_onboarding_label_v2 import SettingsOnboardingLabelV2
from ui.onboarding_page_v2 import OnboardingPageV2


@final
class SettingsOnboardingPageV2(OnboardingPageV2):
    @default_object(SettingsOnboardingLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(
            logger, parent_viewport,
            shader=from_files_names('shaders/shader.vert', 'shaders/onboarding_page/settings_onboarding_page.frag')
        )
