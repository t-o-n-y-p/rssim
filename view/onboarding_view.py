from logging import getLogger

from view import *
from ui.page_control.onboarding_page_control import OnboardingPageControl
from ui.button.skip_onboarding_button import SkipOnboardingButton
from ui.shader_sprite.onboarding_view_shader_sprite import OnboardingViewShaderSprite
from ui.label.skip_onboarding_label import SkipOnboardingLabel


@final
class OnboardingView(View):
    def __init__(self):
        def on_skip_onboarding(button):
            self.controller.parent_controller.on_close_onboarding()

        super().__init__(logger=getLogger('root.app.onboarding.view'))
        self.onboarding_page_control = OnboardingPageControl(parent_viewport=self.viewport)
        self.skip_onboarding_button = SkipOnboardingButton(on_click_action=on_skip_onboarding,
                                                           parent_viewport=self.viewport)
        self.buttons = [*self.onboarding_page_control.buttons, self.skip_onboarding_button]
        self.shader_sprite = OnboardingViewShaderSprite(view=self)
        self.skip_onboarding_label = SkipOnboardingLabel(parent_viewport=self.viewport)

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.skip_onboarding_label.create()
        self.onboarding_page_control.on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.onboarding_page_control.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.onboarding_page_control.on_change_screen_resolution(self.screen_resolution)
        self.skip_onboarding_label.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.onboarding_page_control.on_update_current_locale(self.current_locale)
        self.skip_onboarding_label.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.skip_onboarding_label.on_update_opacity(self.opacity)
        self.onboarding_page_control.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
        self.onboarding_page_control.on_apply_shaders_and_draw_vertices()
