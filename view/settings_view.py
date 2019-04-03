from logging import getLogger
from ctypes import windll

from view import *
from ui.button.accept_settings_button import AcceptSettingsButton
from ui.button.reject_settings_button import RejectSettingsButton
from ui.settings.enum_value_control.screen_resolution_control import ScreenResolutionControl
from ui.settings.checkbox.display_fps_checkbox import DisplayFPSCheckbox
from ui.settings.checkbox_group.notifications_checkbox_group import NotificationsCheckboxGroup


class SettingsView(View):
    """
    Implements Settings view.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        def on_accept_changes(button):
            """
            Notifies controller that player accepts changes.

            :param button:                      button that was clicked
            """
            self.controller.on_save_and_commit_state()
            self.controller.on_deactivate()

        def on_reject_changes(button):
            """
            Notifies controller that player rejects changes.

            :param button:                      button that was clicked
            """
            self.controller.on_deactivate()

        def on_update_windowed_resolution_state(index):
            self.on_change_temp_windowed_resolution(self.available_windowed_resolutions[index])

        def on_update_display_fps_state(new_state):
            self.temp_display_fps = new_state

        def on_update_level_up_notifications_state(new_state):
            self.temp_level_up_notification_enabled = new_state

        def on_update_feature_unlocked_notifications_state(new_state):
            self.temp_feature_unlocked_notification_enabled = new_state

        def on_update_construction_completed_notifications_state(new_state):
            self.temp_construction_completed_notification_enabled = new_state

        def on_update_enough_money_notifications_state(new_state):
            self.temp_enough_money_notification_enabled = new_state

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.settings.view'))
        self.temp_windowed_resolution = (0, 0)
        self.temp_display_fps = False
        self.display_fps_checkbox \
            = DisplayFPSCheckbox(-1, -3, self.surface, self.batches, self.groups, self.current_locale,
                                 on_update_state_action=on_update_display_fps_state)
        self.temp_level_up_notification_enabled = False
        self.temp_feature_unlocked_notification_enabled = False
        self.temp_construction_completed_notification_enabled = False
        self.temp_enough_money_notification_enabled = False
        self.notifications_checkbox_group \
            = NotificationsCheckboxGroup(1, 4, self.surface, self.batches, self.groups, self.current_locale,
                                         on_update_state_actions=[on_update_level_up_notifications_state,
                                                                  on_update_feature_unlocked_notifications_state,
                                                                  on_update_construction_completed_notifications_state,
                                                                  on_update_enough_money_notifications_state])
        self.temp_log_level = 0
        self.settings_opacity = 0
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
        self.available_windowed_resolutions_position = 0
        self.screen_resolution_control \
            = ScreenResolutionControl(-1, 3, self.surface, self.batches, self.groups, self.current_locale,
                                      possible_values_list=self.available_windowed_resolutions,
                                      on_update_state_action=on_update_windowed_resolution_state)
        self.accept_settings_button = AcceptSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_accept_changes)
        self.buttons.append(self.accept_settings_button)
        self.reject_settings_button = RejectSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_reject_changes)
        self.buttons.append(self.reject_settings_button)
        self.buttons.extend(self.screen_resolution_control.buttons)

    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        if self.is_activated and self.settings_opacity < 255:
            self.settings_opacity += 15

        if not self.is_activated and self.settings_opacity > 0:
            self.settings_opacity -= 15

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.screen_resolution_control.on_activate()
        self.screen_resolution_control.on_init_state(self.available_windowed_resolutions_position)
        self.display_fps_checkbox.on_activate()
        self.display_fps_checkbox.on_init_state(self.temp_display_fps)
        self.notifications_checkbox_group.on_activate()
        self.notifications_checkbox_group.on_init_state([self.temp_level_up_notification_enabled,
                                                         self.temp_feature_unlocked_notification_enabled,
                                                         self.temp_construction_completed_notification_enabled,
                                                         self.temp_enough_money_notification_enabled])
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.screen_resolution_control.on_deactivate()
        self.display_fps_checkbox.on_deactivate()
        self.notifications_checkbox_group.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.screen_resolution_control.on_change_screen_resolution(screen_resolution)
        self.display_fps_checkbox.on_change_screen_resolution(screen_resolution)
        self.notifications_checkbox_group.on_change_screen_resolution(screen_resolution)
        self.accept_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height * 2 + 2
        self.accept_settings_button.y_margin = 0
        self.accept_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.reject_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.reject_settings_button.y_margin = 0
        self.reject_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        """
        Updates temp windowed resolution and text label for it, windowed resolution position.
        Activates and deactivates windowed resolution buttons if needed.

        :param windowed_resolution:             selected windowed resolution
        """
        self.temp_windowed_resolution = windowed_resolution
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.screen_resolution_control.on_update_current_locale(new_locale)
        self.display_fps_checkbox.on_update_current_locale(new_locale)
        self.notifications_checkbox_group.on_update_current_locale(new_locale)
