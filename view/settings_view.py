from logging import getLogger

from ui.settings.checkbox.announcements_enabled_checkbox import AnnouncementsEnabledCheckbox
from ui.settings.checkbox_group.malfunction_notifications_checkbox_group import MalfunctionNotificationsCheckboxGroup
from ui.settings.knob.master_volume_settings_knob import MasterVolumeSettingsKnob
from view import *
from ui.button.accept_settings_button import AcceptSettingsButton
from ui.button.reject_settings_button import RejectSettingsButton
from ui.settings.enum_value_control.screen_resolution_control import ScreenResolutionControl
from ui.settings.checkbox.display_fps_checkbox import DisplayFPSCheckbox
from ui.settings.checkbox.fade_animations_enabled_checkbox import FadeAnimationsEnabledCheckbox
from ui.settings.checkbox.clock_24h_checkbox import Clock24HCheckbox
from ui.settings.checkbox_group.game_progress_notifications_checkbox_group import GameProgressNotificationsCheckboxGroup
from ui.shader_sprite.settings_view_shader_sprite import SettingsViewShaderSprite


@final
class SettingsView(AppBaseView):
    def __init__(self, controller):
        def on_accept_changes(button):
            self.controller.parent_controller.on_accept_changes(
                self.temp_windowed_resolution, self.temp_display_fps,
                self.temp_fade_animations_enabled, self.temp_clock_24h_enabled,
                self.temp_level_up_notification_enabled, self.temp_feature_unlocked_notification_enabled,
                self.temp_construction_completed_notification_enabled, self.temp_enough_money_notification_enabled,
                self.temp_bonus_expired_notification_enabled, self.temp_shop_storage_notification_enabled,
                self.temp_voice_not_found_notification_enabled,
                self.temp_master_volume, self.temp_announcements_enabled
            )
            self.controller.on_save_and_commit_state()
            self.controller.parent_controller.on_close_settings()

        def on_reject_changes(button):
            self.controller.parent_controller.on_close_settings()

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

        def on_update_voice_not_found_notifications_state(new_state):
            self.temp_voice_not_found_notification_enabled = new_state

        def on_update_master_volume(master_volume):
            self.temp_master_volume = master_volume

        def on_update_announcements_state(new_state):
            self.temp_announcements_enabled = new_state

        super().__init__(controller, logger=getLogger('root.app.settings.view'))
        self.temp_windowed_resolution = (0, 0)
        self.temp_display_fps = FALSE
        self.temp_fade_animations_enabled = FALSE
        self.temp_clock_24h_enabled = FALSE
        self.temp_master_volume = 0
        self.temp_announcements_enabled = TRUE
        self.display_fps_checkbox \
            = DisplayFPSCheckbox(column=-1, row=2, on_update_state_action=on_update_display_fps_state,
                                 parent_viewport=self.viewport)
        self.fade_animations_checkbox = FadeAnimationsEnabledCheckbox(
            column=-1, row=0, on_update_state_action=on_update_fade_animations_state, parent_viewport=self.viewport
        )
        self.clock_24h_checkbox = Clock24HCheckbox(
            column=-1, row=-2, on_update_state_action=on_update_clock_24h_state, parent_viewport=self.viewport
        )
        self.master_volume_knob = MasterVolumeSettingsKnob(
            column=-1, row=-5, on_update_state_action=on_update_master_volume, parent_viewport=self.viewport
        )
        self.announcements_checkbox = AnnouncementsEnabledCheckbox(
            column=-1, row=-8, on_update_state_action=on_update_announcements_state, parent_viewport=self.viewport
        )
        self.temp_level_up_notification_enabled = FALSE
        self.temp_feature_unlocked_notification_enabled = FALSE
        self.temp_construction_completed_notification_enabled = FALSE
        self.temp_enough_money_notification_enabled = FALSE
        self.temp_bonus_expired_notification_enabled = FALSE
        self.temp_shop_storage_notification_enabled = FALSE
        self.temp_voice_not_found_notification_enabled = FALSE
        self.game_progress_notifications_checkbox_group = GameProgressNotificationsCheckboxGroup(
            column=1, row=9, on_update_state_actions=[
                on_update_level_up_notifications_state,
                on_update_feature_unlocked_notifications_state,
                on_update_construction_completed_notifications_state,
                on_update_enough_money_notifications_state,
                on_update_bonus_expired_notifications_state,
                on_update_shop_storage_notifications_state
            ], parent_viewport=self.viewport
        )
        self.malfunction_notifications_checkbox_group = MalfunctionNotificationsCheckboxGroup(
            column=1, row=-7, on_update_state_actions=[
                on_update_voice_not_found_notifications_state
            ], parent_viewport=self.viewport
        )
        CONFIG_DB_CURSOR.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                    WHERE manual_setup = 1 AND app_width <= ?''',
                                 (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = CONFIG_DB_CURSOR.fetchall()
        self.available_windowed_resolutions_position = 0
        self.screen_resolution_control \
            = ScreenResolutionControl(column=-1, row=8, possible_values_list=self.available_windowed_resolutions,
                                      on_update_state_action=on_update_windowed_resolution_state,
                                      parent_viewport=self.viewport)
        self.accept_settings_button = AcceptSettingsButton(on_click_action=on_accept_changes,
                                                           parent_viewport=self.viewport)
        self.reject_settings_button = RejectSettingsButton(on_click_action=on_reject_changes,
                                                           parent_viewport=self.viewport)
        self.buttons = [self.accept_settings_button, self.reject_settings_button,
                        *self.screen_resolution_control.buttons, *self.display_fps_checkbox.buttons,
                        *self.fade_animations_checkbox.buttons, *self.clock_24h_checkbox.buttons,
                        *self.game_progress_notifications_checkbox_group.buttons,
                        *self.malfunction_notifications_checkbox_group.buttons,
                        *self.announcements_checkbox.buttons]
        self.shader_sprite = SettingsViewShaderSprite(view=self)
        self.on_mouse_motion_handlers.extend(self.master_volume_knob.on_mouse_motion_handlers)
        self.on_mouse_press_handlers.extend(self.master_volume_knob.on_mouse_press_handlers)
        self.on_mouse_release_handlers.extend(self.master_volume_knob.on_mouse_release_handlers)
        self.on_mouse_drag_handlers.extend(self.master_volume_knob.on_mouse_drag_handlers)
        self.on_window_resize_handlers.extend([
            *self.display_fps_checkbox.on_window_resize_handlers,
            *self.fade_animations_checkbox.on_window_resize_handlers,
            *self.clock_24h_checkbox.on_window_resize_handlers,
            *self.game_progress_notifications_checkbox_group.on_window_resize_handlers,
            *self.malfunction_notifications_checkbox_group.on_window_resize_handlers,
            *self.screen_resolution_control.on_window_resize_handlers,
            *self.master_volume_knob.on_window_resize_handlers,
            *self.announcements_checkbox.on_window_resize_handlers,
            self.shader_sprite.on_window_resize
        ])
        self.on_append_window_handlers()

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
        self.temp_windowed_resolution = USER_DB_CURSOR.fetchone()
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)
        self.screen_resolution_control.on_activate()
        self.screen_resolution_control.on_init_state(self.available_windowed_resolutions_position)
        USER_DB_CURSOR.execute('SELECT display_fps, fade_animations_enabled FROM graphics')
        self.temp_display_fps, self.temp_fade_animations_enabled = USER_DB_CURSOR.fetchone()
        self.display_fps_checkbox.on_activate()
        self.display_fps_checkbox.on_change_state(self.temp_display_fps)
        self.fade_animations_checkbox.on_activate()
        self.fade_animations_checkbox.on_change_state(self.temp_fade_animations_enabled)
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.temp_clock_24h_enabled = USER_DB_CURSOR.fetchone()[0]
        self.clock_24h_checkbox.on_activate()
        self.clock_24h_checkbox.on_change_state(self.temp_clock_24h_enabled)
        USER_DB_CURSOR.execute('SELECT * FROM notification_settings')
        self.temp_level_up_notification_enabled, self.temp_feature_unlocked_notification_enabled, \
            self.temp_construction_completed_notification_enabled, self.temp_enough_money_notification_enabled, \
            self.temp_bonus_expired_notification_enabled, self.temp_shop_storage_notification_enabled, \
            self.temp_voice_not_found_notification_enabled = USER_DB_CURSOR.fetchone()
        self.game_progress_notifications_checkbox_group.on_activate()
        self.game_progress_notifications_checkbox_group.on_change_state(
            [
                self.temp_level_up_notification_enabled,
                self.temp_feature_unlocked_notification_enabled,
                self.temp_construction_completed_notification_enabled,
                self.temp_enough_money_notification_enabled,
                self.temp_bonus_expired_notification_enabled,
                self.temp_shop_storage_notification_enabled
            ]
        )
        self.malfunction_notifications_checkbox_group.on_activate()
        self.malfunction_notifications_checkbox_group.on_change_state(
            [
                self.temp_voice_not_found_notification_enabled
            ]
        )
        USER_DB_CURSOR.execute('''SELECT master_volume, announcements_enabled FROM sound''')
        self.temp_master_volume, self.temp_announcements_enabled = USER_DB_CURSOR.fetchone()
        self.master_volume_knob.on_activate()
        self.master_volume_knob.on_init_state(self.temp_master_volume)
        self.announcements_checkbox.on_activate()
        self.announcements_checkbox.on_change_state(self.temp_announcements_enabled)
        self.shader_sprite.create()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.screen_resolution_control.on_deactivate()
        self.display_fps_checkbox.on_deactivate()
        self.fade_animations_checkbox.on_deactivate()
        self.clock_24h_checkbox.on_deactivate()
        self.game_progress_notifications_checkbox_group.on_deactivate()
        self.malfunction_notifications_checkbox_group.on_deactivate()
        self.master_volume_knob.on_deactivate()
        self.announcements_checkbox.on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.screen_resolution_control.on_update_current_locale(self.current_locale)
        self.display_fps_checkbox.on_update_current_locale(self.current_locale)
        self.fade_animations_checkbox.on_update_current_locale(self.current_locale)
        self.clock_24h_checkbox.on_update_current_locale(self.current_locale)
        self.game_progress_notifications_checkbox_group.on_update_current_locale(self.current_locale)
        self.malfunction_notifications_checkbox_group.on_update_current_locale(self.current_locale)
        self.master_volume_knob.on_update_current_locale(self.current_locale)
        self.announcements_checkbox.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.screen_resolution_control.on_update_opacity(self.opacity)
        self.display_fps_checkbox.on_update_opacity(self.opacity)
        self.fade_animations_checkbox.on_update_opacity(self.opacity)
        self.clock_24h_checkbox.on_update_opacity(self.opacity)
        self.game_progress_notifications_checkbox_group.on_update_opacity(self.opacity)
        self.malfunction_notifications_checkbox_group.on_update_opacity(self.opacity)
        self.master_volume_knob.on_update_opacity(self.opacity)
        self.announcements_checkbox.on_update_opacity(self.opacity)

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        self.temp_windowed_resolution = windowed_resolution
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)

    def on_update_clock_state(self, clock_24h_enabled):
        super().on_update_clock_state(clock_24h_enabled)
        self.temp_clock_24h_enabled = clock_24h_enabled
        self.clock_24h_checkbox.on_change_state(self.temp_clock_24h_enabled)
