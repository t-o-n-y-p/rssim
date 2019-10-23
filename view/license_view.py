from logging import getLogger

from view import *
from ui.page_control.license_page_control import LicensePageControl
from ui.button.close_license_button import CloseLicenseButton
from ui.label.close_license_label import CloseLicenseLabel
from ui.shader_sprite.license_view_shader_sprite import LicenseViewShaderSprite


@final
class LicenseView(AppBaseView):
    def __init__(self):
        def on_close_license(button):
            self.controller.parent_controller.on_close_license()

        super().__init__(logger=getLogger('root.app.license.view'))
        self.license_page_control = LicensePageControl(parent_viewport=self.viewport)
        self.close_license_button = CloseLicenseButton(on_click_action=on_close_license, parent_viewport=self.viewport)
        self.buttons = [*self.license_page_control.buttons, self.close_license_button]
        self.close_license_label = CloseLicenseLabel(parent_viewport=self.viewport)
        self.shader_sprite = LicenseViewShaderSprite(view=self)
        self.on_mouse_scroll_handlers = self.license_page_control.on_mouse_scroll_handlers

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.close_license_label.create()
        self.license_page_control.on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.license_page_control.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.close_license_label.on_change_screen_resolution(self.screen_resolution)
        self.license_page_control.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.close_license_label.on_update_current_locale(self.current_locale)
        self.license_page_control.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.close_license_label.on_update_opacity(self.opacity)
        self.license_page_control.on_update_opacity(self.opacity)
