from logging import getLogger
from typing import final

from ui.page_control import *
from ui.onboarding_page.clock_onboarding_page import ClockOnboardingPage
from ui.onboarding_page.constructor_onboarding_page import ConstructorOnboardingPage
from ui.onboarding_page.exp_money_onboarding_page import ExpMoneyOnboardingPage
from ui.onboarding_page.map_onboarding_page import MapOnboardingPage
from ui.onboarding_page.pause_resume_onboarding_page import PauseResumeOnboardingPage
from ui.onboarding_page.schedule_onboarding_page import ScheduleOnboardingPage
from ui.onboarding_page.settings_onboarding_page import SettingsOnboardingPage
from ui.onboarding_page.zoom_onboarding_page import ZoomOnboardingPage
from ui.shader_sprite.onboarding_page_control_shader_sprite import OnboardingPageControlShaderSprite


@final
class OnboardingPageControl(PageControl):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.app.onboarding.view.onboarding_page_control'),
                         parent_viewport=parent_viewport)
        self.pages = [MapOnboardingPage(parent_viewport=self.viewport),
                      ZoomOnboardingPage(parent_viewport=self.viewport),
                      ConstructorOnboardingPage(parent_viewport=self.viewport),
                      ExpMoneyOnboardingPage(parent_viewport=self.viewport),
                      ScheduleOnboardingPage(parent_viewport=self.viewport),
                      PauseResumeOnboardingPage(parent_viewport=self.viewport),
                      ClockOnboardingPage(parent_viewport=self.viewport),
                      SettingsOnboardingPage(parent_viewport=self.viewport)]
        self.shader_sprite = OnboardingPageControlShaderSprite(view=self)

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
