from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.button.accept_settings_button import AcceptSettingsButton
from ui.button.reject_settings_button import RejectSettingsButton
from ui.settings.enum_value_control.screen_resolution_control import ScreenResolutionControl
from ui.settings.checkbox.display_fps_checkbox import DisplayFPSCheckbox
from ui.settings.checkbox.fade_animations_enabled_checkbox import FadeAnimationsEnabledCheckbox
from ui.settings.checkbox.clock_24h_checkbox import Clock24HCheckbox
from ui.settings.checkbox_group.notifications_checkbox_group import NotificationsCheckboxGroup
from ui.shader_sprite.settings_view_shader_sprite import SettingsViewShaderSprite


class SettingsView(View):
    def __init__(self):
        def on_accept_changes(button):
            self.controller.on_save_and_commit_state()
            if self.controller.navigated_from_main_menu:
                self.controller.navigated_from_main_menu = False
                self.controller.parent_controller.main_menu_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_main_menu_transition_animation.on_activate()

            if self.controller.navigated_from_game:
                self.controller.navigated_from_game = False
                self.controller.parent_controller.game_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_game_transition_animation.on_activate()

        def on_reject_changes(button):
            if self.controller.navigated_from_main_menu:
                self.controller.navigated_from_main_menu = False
                self.controller.parent_controller.main_menu_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_main_menu_transition_animation.on_activate()

            if self.controller.navigated_from_game:
                self.controller.navigated_from_game = False
                self.controller.parent_controller.game_to_settings_transition_animation.on_deactivate()
                self.controller.parent_controller.settings_to_game_transition_animation.on_activate()

        def on_update_windowed_resolution_state(index):
            self.on_change_temp_windowed_resolution(self.available_windowed_resolutions[index])

        def on_update_display_fps_state(new_state):
            self.temp_display_fps = new_state

        def on_update_fade_animations_state(new_state):
            self.temp_fade_animations_enabled = new_state

        def on_update_clock_24h_state(new_state):
            self.temp_clock_24h_enabled = new_state

        def on_update_level_up_notifications_state(new_state):
            self.temp_level_up_notification_enabled = new_state

        def on_update_feature_unlocked_notifications_state(new_state):
            self.temp_feature_unlocked_notification_enabled = new_state

        def on_update_construction_completed_notifications_state(new_state):
            self.temp_construction_completed_notification_enabled = new_state

        def on_update_enough_money_notifications_state(new_state):
            self.temp_enough_money_notification_enabled = new_state

        def on_update_bonus_expired_notifications_state(new_state):
            self.temp_bonus_expired_notification_enabled = new_state

        def on_update_shop_storage_notifications_state(new_state):
            self.temp_shop_storage_notification_enabled = new_state

        super().__init__(logger=getLogger('root.app.settings.view'))
        self.temp_windowed_resolution = (0, 0)
        self.temp_display_fps = False
        self.temp_fade_animations_enabled = False
        self.temp_clock_24h_enabled = False
        self.display_fps_checkbox \
            = DisplayFPSCheckbox(column=-1, row=-1, on_update_state_action=on_update_display_fps_state,
                                 parent_viewport=self.viewport)
        self.fade_animations_checkbox \
            = FadeAnimationsEnabledCheckbox(column=-1, row=-3, on_update_state_action=on_update_fade_animations_state,
                                            parent_viewport=self.viewport)
        self.clock_24h_checkbox = Clock24HCheckbox(column=-1, row=-5, on_update_state_action=on_update_clock_24h_state,
                                                   parent_viewport=self.viewport)
        self.temp_level_up_notification_enabled = False
        self.temp_feature_unlocked_notification_enabled = False
        self.temp_construction_completed_notification_enabled = False
        self.temp_enough_money_notification_enabled = False
        self.temp_bonus_expired_notification_enabled = False
        self.temp_shop_storage_notification_enabled = False
        self.notifications_checkbox_group \
            = NotificationsCheckboxGroup(column=1, row=6,
                                         on_update_state_actions=[on_update_level_up_notifications_state,
                                                                  on_update_feature_unlocked_notifications_state,
                                                                  on_update_construction_completed_notifications_state,
                                                                  on_update_enough_money_notifications_state,
                                                                  on_update_bonus_expired_notifications_state,
                                                                  on_update_shop_storage_notifications_state],
                                         parent_viewport=self.viewport)
        self.temp_log_level = 0
        CONFIG_DB_CURSOR.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                    WHERE manual_setup = 1 AND app_width <= ?''',
                                 (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = CONFIG_DB_CURSOR.fetchall()
        self.available_windowed_resolutions_position = 0
        self.screen_resolution_control \
            = ScreenResolutionControl(column=-1, row=5, possible_values_list=self.available_windowed_resolutions,
                                      on_update_state_action=on_update_windowed_resolution_state,
                                      parent_viewport=self.viewport)
        self.accept_settings_button = AcceptSettingsButton(on_click_action=on_accept_changes,
                                                           parent_viewport=self.viewport)
        self.reject_settings_button = RejectSettingsButton(on_click_action=on_reject_changes,
                                                           parent_viewport=self.viewport)
        self.buttons = [self.accept_settings_button, self.reject_settings_button,
                        *self.screen_resolution_control.buttons, *self.display_fps_checkbox.buttons,
                        *self.fade_animations_checkbox.buttons, *self.clock_24h_checkbox.buttons,
                        *self.notifications_checkbox_group.buttons]
        self.shader_sprite = SettingsViewShaderSprite(view=self)

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
        self.screen_resolution_control.on_activate()
        self.screen_resolution_control.on_init_state(self.available_windowed_resolutions_position)
        self.display_fps_checkbox.on_activate()
        self.display_fps_checkbox.on_init_state(self.temp_display_fps)
        self.fade_animations_checkbox.on_activate()
        self.fade_animations_checkbox.on_init_state(self.temp_fade_animations_enabled)
        self.clock_24h_checkbox.on_activate()
        self.clock_24h_checkbox.on_init_state(self.temp_clock_24h_enabled)
        self.notifications_checkbox_group.on_activate()
        self.notifications_checkbox_group.on_init_state([self.temp_level_up_notification_enabled,
                                                         self.temp_feature_unlocked_notification_enabled,
                                                         self.temp_construction_completed_notification_enabled,
                                                         self.temp_enough_money_notification_enabled,
                                                         self.temp_bonus_expired_notification_enabled,
                                                         self.temp_shop_storage_notification_enabled])
        self.shader_sprite.create()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.screen_resolution_control.on_deactivate()
        self.display_fps_checkbox.on_deactivate()
        self.fade_animations_checkbox.on_deactivate()
        self.clock_24h_checkbox.on_deactivate()
        self.notifications_checkbox_group.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.screen_resolution_control.on_change_screen_resolution(self.screen_resolution)
        self.display_fps_checkbox.on_change_screen_resolution(self.screen_resolution)
        self.fade_animations_checkbox.on_change_screen_resolution(self.screen_resolution)
        self.clock_24h_checkbox.on_change_screen_resolution(self.screen_resolution)
        self.notifications_checkbox_group.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.screen_resolution_control.on_update_current_locale(self.current_locale)
        self.display_fps_checkbox.on_update_current_locale(self.current_locale)
        self.fade_animations_checkbox.on_update_current_locale(self.current_locale)
        self.clock_24h_checkbox.on_update_current_locale(self.current_locale)
        self.notifications_checkbox_group.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.screen_resolution_control.on_update_opacity(self.opacity)
        self.display_fps_checkbox.on_update_opacity(self.opacity)
        self.fade_animations_checkbox.on_update_opacity(self.opacity)
        self.clock_24h_checkbox.on_update_opacity(self.opacity)
        self.notifications_checkbox_group.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        self.temp_windowed_resolution = windowed_resolution
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
