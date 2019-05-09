from logging import getLogger

from pyshaders import from_files_names

from ui.page_control import *
from ui.onboarding_page.clock_onboarding_page import ClockOnboardingPage
from ui.onboarding_page.constructor_onboarding_page import ConstructorOnboardingPage
from ui.onboarding_page.exp_money_onboarding_page import ExpMoneyOnboardingPage
from ui.onboarding_page.map_onboarding_page import MapOnboardingPage
from ui.onboarding_page.pause_resume_onboarding_page import PauseResumeOnboardingPage
from ui.onboarding_page.schedule_onboarding_page import ScheduleOnboardingPage
from ui.onboarding_page.settings_onboarding_page import SettingsOnboardingPage
from ui.onboarding_page.zoom_onboarding_page import ZoomOnboardingPage


class OnboardingPageControl(PageControl):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.view.onboarding_page_control'))
        self.pages = [MapOnboardingPage(), ZoomOnboardingPage(), ConstructorOnboardingPage(), ExpMoneyOnboardingPage(),
                      ScheduleOnboardingPage(), PauseResumeOnboardingPage(), ClockOnboardingPage(),
                      SettingsOnboardingPage()]
        self.shader = from_files_names('shaders/shader.vert', 'shaders/onboarding_page_control/shader.frag')
        self.shader_sprite = None

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.onboarding_page_control_opacity = self.opacity
        self.shader.uniforms.position = self.pages[self.current_page].position
        self.shader.uniforms.size = self.pages[self.current_page].size
        self.shader.uniforms.page_number = self.current_page
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()
