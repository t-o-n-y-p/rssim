from logging import getLogger

from view import *
from ui.button.create_station_button import CreateStationButton
from ui.button.back_to_the_station_button import BackToTheStationButton
from ui.button.open_license_button import OpenLicenseButton
from ui.button.open_settings_main_menu_view_button import OpenSettingsMainMenuViewButton
from ui.label.open_license_label import OpenLicenseLabel
from ui.button.enter_code_button import EnterCodeButton
from ui.shader_sprite.main_menu_view_shader_sprite import MainMenuViewShaderSprite


@final
class MainMenuView(AppBaseView):
    def __init__(self, controller):
        def on_create_station(button):
            self.controller.parent_controller.on_open_onboarding()

        def on_back_to_the_station(button):
            self.controller.parent_controller.on_back_to_the_station()

        def on_open_license(button):
            self.controller.parent_controller.on_open_license()

        def on_open_settings(button):
            self.controller.parent_controller.on_open_settings_from_main_menu()

        def on_open_bonus_code(button):
            self.controller.parent_controller.on_open_bonus_code()

        super().__init__(controller, logger=getLogger('root.app.main_menu.view'))
        self.create_station_button = CreateStationButton(on_click_action=on_create_station,
                                                         parent_viewport=self.viewport)
        self.back_to_the_station_button = BackToTheStationButton(on_click_action=on_back_to_the_station,
                                                                 parent_viewport=self.viewport)
        self.open_license_button = OpenLicenseButton(on_click_action=on_open_license, parent_viewport=self.viewport)
        self.open_settings_button = OpenSettingsMainMenuViewButton(on_click_action=on_open_settings,
                                                                   parent_viewport=self.viewport)
        self.enter_code_button = EnterCodeButton(on_click_action=on_open_bonus_code, parent_viewport=self.viewport)
        self.buttons = [self.create_station_button, self.back_to_the_station_button, self.open_license_button,
                        self.open_settings_button, self.enter_code_button]
        self.open_license_label = OpenLicenseLabel(parent_viewport=self.viewport)
        self.shader_sprite = MainMenuViewShaderSprite(view=self)
        self.on_window_resize_handlers.extend([
            self.shader_sprite.on_window_resize, self.open_license_label.on_window_resize
        ])
        self.on_append_window_handlers()

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.open_license_label.create()
        USER_DB_CURSOR.execute('SELECT onboarding_required, bonus_codes_locked FROM game_progress')
        onboarding_required, bonus_codes_locked = USER_DB_CURSOR.fetchone()
        if onboarding_required:
            self.create_station_button.on_activate()
        else:
            self.back_to_the_station_button.on_activate()

        if not bonus_codes_locked:
            self.enter_code_button.on_activate()
        else:
            self.enter_code_button.on_disable()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.create_station_button.on_update_current_locale(self.current_locale)
        self.back_to_the_station_button.on_update_current_locale(self.current_locale)
        self.open_settings_button.on_update_current_locale(self.current_locale)
        self.open_license_label.on_update_current_locale(self.current_locale)
        self.enter_code_button.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.open_license_label.on_update_opacity(self.opacity)
