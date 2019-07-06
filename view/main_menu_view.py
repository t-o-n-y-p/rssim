from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.button.create_station_button import CreateStationButton
from ui.button.back_to_the_station_button import BackToTheStationButton
from ui.button.open_license_button import OpenLicenseButton
from ui.shader_sprite.main_menu_view_shader_sprite import MainMenuViewShaderSprite


class MainMenuView(View):
    def __init__(self):
        def on_create_station(button):
            button.on_deactivate()
            self.controller.parent_controller.license_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.main_menu_to_onboarding_transition_animation.on_activate()

        def on_back_to_the_station(button):
            button.on_deactivate()
            self.controller.parent_controller.license_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_main_menu_transition_animation.on_deactivate()
            self.controller.parent_controller.main_menu_to_game_transition_animation.on_activate()
            self.controller.parent_controller.on_resume_game()

        def on_open_license(button):
            button.on_deactivate()
            self.controller.parent_controller.on_open_license()

        super().__init__(logger=getLogger('root.app.main_menu.view'))
        self.create_station_button = CreateStationButton(on_click_action=on_create_station,
                                                         parent_viewport=self.viewport)
        self.back_to_the_station_button = BackToTheStationButton(on_click_action=on_back_to_the_station,
                                                                 parent_viewport=self.viewport)
        self.open_license_button = OpenLicenseButton(on_click_action=on_open_license,
                                                     parent_viewport=self.viewport)
        self.buttons = [self.create_station_button, self.back_to_the_station_button, self.open_license_button]
        self.shader_sprite = MainMenuViewShaderSprite(view=self)
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
        USER_DB_CURSOR.execute('SELECT onboarding_required FROM game_progress')
        onboarding_required = bool(USER_DB_CURSOR.fetchone()[0])
        if onboarding_required:
            self.create_station_button.on_activate()
        else:
            self.back_to_the_station_button.on_activate()

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.create_station_button.on_update_current_locale(self.current_locale)
        self.back_to_the_station_button.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
