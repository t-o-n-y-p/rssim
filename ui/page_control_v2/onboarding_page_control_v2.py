from typing import final

from ui import default_object, optional_object
from ui.onboarding_page_v2.clock_onboarding_page_v2 import ClockOnboardingPageV2
from ui.onboarding_page_v2.constructor_onboarding_page_v2 import ConstructorOnboardingPageV2
from ui.onboarding_page_v2.exp_money_onboarding_page_v2 import ExpMoneyOnboardingPageV2
from ui.onboarding_page_v2.map_onboarding_page_v2 import MapOnboardingPageV2
from ui.onboarding_page_v2.map_switcher_onboarding_page_v2 import MapSwitcherOnboardingPageV2
from ui.onboarding_page_v2.schedule_onboarding_page_v2 import ScheduleOnboardingPageV2
from ui.onboarding_page_v2.settings_onboarding_page_v2 import SettingsOnboardingPageV2
from ui.page_control_v2 import PageControlV2


@final
class OnboardingPageControlV2(PageControlV2):
    @default_object(MapOnboardingPageV2)
    @optional_object(MapSwitcherOnboardingPageV2)
    @optional_object(ConstructorOnboardingPageV2)
    @optional_object(ExpMoneyOnboardingPageV2)
    @optional_object(ScheduleOnboardingPageV2)
    @optional_object(ClockOnboardingPageV2)
    @optional_object(SettingsOnboardingPageV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
