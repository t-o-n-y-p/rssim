from logging import getLogger
from typing import final

from ui.page_control.onboarding_page_control import OnboardingPageControl
from ui.button.skip_onboarding_button import SkipOnboardingButton
from ui.shader_sprite.onboarding_view_shader_sprite import OnboardingViewShaderSprite
from ui.label.skip_onboarding_label import SkipOnboardingLabel
from view import AppBaseView, view_is_not_active, view_is_active


@final
class OnboardingView(AppBaseView):
    def __init__(self, controller):
        def on_skip_onboarding(button):
            self.controller.parent_controller.on_close_onboarding()

        super().__init__(controller, logger=getLogger('root.app.onboarding.view'))
        self.onboarding_page_control = OnboardingPageControl(parent_viewport=self.viewport)
        self.skip_onboarding_button = SkipOnboardingButton(
            on_click_action=on_skip_onboarding, parent_viewport=self.viewport
        )
        self.buttons = [*self.onboarding_page_control.buttons, self.skip_onboarding_button]
        self.shader_sprite = OnboardingViewShaderSprite(view=self)
        self.skip_onboarding_label = SkipOnboardingLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend(
            [
                *self.onboarding_page_control.on_window_resize_handlers,
                self.shader_sprite.on_window_resize, self.skip_onboarding_label.on_window_resize
            ]
        )
        self.on_append_window_handlers()

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

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.onboarding_page_control.on_update_current_locale(self.current_locale)
        self.skip_onboarding_label.on_update_current_locale(self.current_locale)

    def on_apply_shaders_and_draw_vertices(self):
        super().on_apply_shaders_and_draw_vertices()
        self.onboarding_page_control.on_apply_shaders_and_draw_vertices()

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.skip_onboarding_label.on_update_opacity(self.opacity)
        self.onboarding_page_control.on_update_opacity(self.opacity)
