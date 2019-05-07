from logging import getLogger

from ui.page_control import PageControl
from ui.onboarding_page.bottom_bar_onboarding_page import BottomBarOnboardingPage
from ui.onboarding_page.constructor_onboarding_page import ConstructorOnboardingPage
from ui.onboarding_page.map_onboarding_page import MapOnboardingPage


class OnboardingPageControl(PageControl):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.onboarding.view.onboarding_page_control'))
        self.pages = [MapOnboardingPage(), BottomBarOnboardingPage(), ConstructorOnboardingPage()]

    def on_apply_shaders_and_draw_vertices(self):
        self.current_page.on_apply_shaders_and_draw_vertices()
