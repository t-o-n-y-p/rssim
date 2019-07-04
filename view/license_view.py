from logging import getLogger

from view import *
from ui.page_control.license_page_control import LicensePageControl
from ui.button.close_license_button import CloseLicenseButton
from ui.shader_sprite.license_view_shader_sprite import LicenseViewShaderSprite


class LicenseView(View):
    def __init__(self):
        def on_close_license(button):
            self.controller.parent_controller.on_close_license()

        super().__init__(logger=getLogger('root.app.license.view'))
        self.license_page_control = LicensePageControl(parent_viewport=self.viewport)
        self.close_license_button = CloseLicenseButton(on_click_action=on_close_license, parent_viewport=self.viewport)
        self.buttons = [*self.license_page_control.buttons, self.close_license_button]
        self.shader_sprite = LicenseViewShaderSprite(view=self)
        self.on_mouse_scroll_handlers = self.license_page_control.on_mouse_scroll_handlers
        self.on_init_content()

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.shader_sprite.create()
        self.license_page_control.on_activate()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.license_page_control.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.license_page_control.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.license_page_control.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.license_page_control.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
