from logging import getLogger
from ctypes import windll

from pyglet.text import Label

from view import *
from button import create_two_state_button
from button.accept_settings_button import AcceptSettingsButton
from button.reject_settings_button import RejectSettingsButton
from button.increment_windowed_resolution_button import IncrementWindowedResolutionButton
from button.decrement_windowed_resolution_button import DecrementWindowedResolutionButton
from button.checked_checkbox_button import CheckedCheckboxButton
from button.unchecked_checkbox_button import UncheckedCheckboxButton
from i18n import I18N_RESOURCES


class SettingsView(View):
    """
    Implements Settings view.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_accept_changes                           on_click handler for accept settings button
            on_reject_changes                           on_click handler for reject settings button
            on_increment_windowed_resolution            on_click handler for increment windowed resolution button
            on_decrement_windowed_resolution            on_click handler for decrement windowed resolution button
            on_click handlers for corresponding checked and unchecked checkbox buttons:
                on_check_level_up_notifications
                on_uncheck_level_up_notifications
                on_check_feature_unlocked_notifications
                on_uncheck_feature_unlocked_notifications
                on_check_construction_completed_notifications
                on_uncheck_construction_completed_notifications
                on_check_enough_money_notifications
                on_uncheck_enough_money_notifications

        Properties:
            temp_windowed_resolution                    windowed resolution selected by player before making decision
            temp_log_level                              log level selected by player before making decision
            medium_line                                 Y position of the middle of settings screen
            settings_opacity                            general opacity for settings screen
            available_windowed_resolutions              list of app window resolutions available in windowed mode
            available_windowed_resolutions_position     position of currently selected windowed resolution
            accept_settings_button                      AcceptSettingsButton object
            reject_settings_button                      RejectSettingsButton object
            increment_windowed_resolution_button        IncrementWindowedResolutionButton object
            decrement_windowed_resolution_button        DecrementWindowedResolutionButton object
            buttons                                     list of all buttons
            temp_windowed_resolution_label              label from temp windowed resolution
            windowed_resolution_description_label       label from windowed resolution setting description
            notification_description_label              label from notifications settings description
            labels from corresponding notification settings description:
                level_up_notification_description_label
                feature_unlocked_notification_description_label
                construction_completed_notification_description_label
                enough_money_notification_description_label
            temp_level_up_notification_enabled
                                level up notification flag value selected by player before making decision
            temp_feature_unlocked_notification_enabled
                                feature unlocked notification flag value selected by player before making decision
            temp_construction_completed_notification_enabled
                                construction completed notification flag value selected by player before making decision
            temp_enough_money_notification_enabled
                                enough money notification flag value selected by player before making decision

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
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

        def on_increment_windowed_resolution(button):
            """
            Updates windowed resolution when user increases it.

            :param button:                      button that was clicked
            """
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position + 1]
            )

        def on_decrement_windowed_resolution(button):
            """
            Updates windowed resolution when user decreases it.

            :param button:                      button that was clicked
            """
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position - 1]
            )

        def on_check_level_up_notifications(button):
            """
            Enables temp level up notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_level_up_notification_enabled = True

        def on_uncheck_level_up_notifications(button):
            """
            Disables temp level up notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_level_up_notification_enabled = False

        def on_check_feature_unlocked_notifications(button):
            """
            Enables temp feature unlocked notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_feature_unlocked_notification_enabled = True

        def on_uncheck_feature_unlocked_notifications(button):
            """
            Disables temp feature unlocked notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_feature_unlocked_notification_enabled = False

        def on_check_construction_completed_notifications(button):
            """
            Enables temp construction completed notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_construction_completed_notification_enabled = True

        def on_uncheck_construction_completed_notifications(button):
            """
            Disables temp construction completed notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_construction_completed_notification_enabled = False

        def on_check_enough_money_notifications(button):
            """
            Enables temp enough money notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_enough_money_notification_enabled = True

        def on_uncheck_enough_money_notifications(button):
            """
            Disables temp enough money notifications flag.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.temp_enough_money_notification_enabled = False

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.settings.view'))
        self.temp_windowed_resolution = (0, 0)
        self.temp_level_up_notification_enabled = False
        self.temp_feature_unlocked_notification_enabled = False
        self.temp_construction_completed_notification_enabled = False
        self.temp_enough_money_notification_enabled = False
        self.temp_log_level = 0
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        self.settings_opacity = 0
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
        self.available_windowed_resolutions_position = 0
        self.accept_settings_button = AcceptSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_accept_changes)
        self.buttons.append(self.accept_settings_button)
        self.reject_settings_button = RejectSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_reject_changes)
        self.buttons.append(self.reject_settings_button)
        self.increment_windowed_resolution_button \
            = IncrementWindowedResolutionButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                groups=self.groups, on_click_action=on_increment_windowed_resolution)
        self.decrement_windowed_resolution_button \
            = DecrementWindowedResolutionButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                groups=self.groups, on_click_action=on_decrement_windowed_resolution)
        self.level_up_checked_checkbox_button, self.level_up_unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(surface=self.surface,
                                                            batch=self.batches['ui_batch'], groups=self.groups,
                                                            on_click_action=on_uncheck_level_up_notifications),
                                      UncheckedCheckboxButton(surface=self.surface,
                                                              batch=self.batches['ui_batch'], groups=self.groups,
                                                              on_click_action=on_check_level_up_notifications))
        self.feature_unlocked_checked_checkbox_button, self.feature_unlocked_unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(surface=self.surface,
                                                            batch=self.batches['ui_batch'], groups=self.groups,
                                                            on_click_action=on_uncheck_feature_unlocked_notifications),
                                      UncheckedCheckboxButton(surface=self.surface,
                                                              batch=self.batches['ui_batch'], groups=self.groups,
                                                              on_click_action=on_check_feature_unlocked_notifications))
        self.construction_completed_checked_checkbox_button, self.construction_completed_unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(surface=self.surface,
                                                            batch=self.batches['ui_batch'], groups=self.groups,
                                                            on_click_action
                                                            =on_uncheck_construction_completed_notifications),
                                      UncheckedCheckboxButton(surface=self.surface,
                                                              batch=self.batches['ui_batch'], groups=self.groups,
                                                              on_click_action
                                                              =on_check_construction_completed_notifications))
        self.enough_money_checked_checkbox_button, self.enough_money_unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(surface=self.surface,
                                                            batch=self.batches['ui_batch'], groups=self.groups,
                                                            on_click_action=on_uncheck_enough_money_notifications),
                                      UncheckedCheckboxButton(surface=self.surface,
                                                              batch=self.batches['ui_batch'], groups=self.groups,
                                                              on_click_action=on_check_enough_money_notifications))
        self.buttons.append(self.increment_windowed_resolution_button)
        self.buttons.append(self.decrement_windowed_resolution_button)
        self.buttons.append(self.level_up_checked_checkbox_button)
        self.buttons.append(self.level_up_unchecked_checkbox_button)
        self.buttons.append(self.feature_unlocked_checked_checkbox_button)
        self.buttons.append(self.feature_unlocked_unchecked_checkbox_button)
        self.buttons.append(self.construction_completed_checked_checkbox_button)
        self.buttons.append(self.construction_completed_unchecked_checkbox_button)
        self.buttons.append(self.enough_money_checked_checkbox_button)
        self.buttons.append(self.enough_money_unchecked_checkbox_button)
        self.temp_windowed_resolution_label = None
        self.windowed_resolution_description_label = None
        self.notification_description_label = None
        self.level_up_notification_description_label = None
        self.feature_unlocked_notification_description_label = None
        self.construction_completed_notification_description_label = None
        self.enough_money_notification_description_label = None

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
        self.temp_windowed_resolution_label \
            = Label('x'.join(str(t) for t in self.temp_windowed_resolution),
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line - int(5 * self.top_bar_height / 8),
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.windowed_resolution_description_label \
            = Label(I18N_RESOURCES['windowed_resolution_description_string'][self.current_locale],
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line + int(5 * self.top_bar_height / 8),
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.temp_windowed_resolution_label.delete()
        self.temp_windowed_resolution_label = None
        self.windowed_resolution_description_label.delete()
        self.windowed_resolution_description_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        if self.is_activated:
            self.temp_windowed_resolution_label.x = self.screen_resolution[0] // 4
            self.temp_windowed_resolution_label.y = self.medium_line - int(5 * self.top_bar_height / 8)
            self.temp_windowed_resolution_label.font_size = int(16 / 80 * self.bottom_bar_height)
            self.windowed_resolution_description_label.x = self.screen_resolution[0] // 4
            self.windowed_resolution_description_label.y = self.medium_line + int(5 * self.top_bar_height / 8)
            self.windowed_resolution_description_label.font_size = int(16 / 80 * self.bottom_bar_height)

        self.accept_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height * 2 + 2
        self.accept_settings_button.y_margin = 0
        self.accept_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                    int(self.accept_settings_button.base_font_size_property
                                                        * self.bottom_bar_height))
        self.reject_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.reject_settings_button.y_margin = 0
        self.reject_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                    int(self.reject_settings_button.base_font_size_property
                                                        * self.bottom_bar_height))
        self.increment_windowed_resolution_button.x_margin \
            = 11 * self.screen_resolution[0] // 32 - self.top_bar_height // 2
        self.increment_windowed_resolution_button.y_margin = self.medium_line - int(9 * self.top_bar_height / 8)
        self.increment_windowed_resolution_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.increment_windowed_resolution_button.base_font_size_property
                                 * self.top_bar_height))
        self.decrement_windowed_resolution_button.x_margin \
            = 5 * self.screen_resolution[0] // 32 - self.top_bar_height // 2
        self.decrement_windowed_resolution_button.y_margin = self.medium_line - int(9 * self.top_bar_height / 8)
        self.decrement_windowed_resolution_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.decrement_windowed_resolution_button.base_font_size_property
                                 * self.top_bar_height))
        self.level_up_checked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.level_up_checked_checkbox_button.y_margin = self.medium_line + int(3 * self.top_bar_height / 4)
        self.level_up_checked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.level_up_checked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.level_up_unchecked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.level_up_unchecked_checkbox_button.y_margin = self.medium_line + int(3 * self.top_bar_height / 4)
        self.level_up_unchecked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.level_up_unchecked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.feature_unlocked_checked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.feature_unlocked_checked_checkbox_button.y_margin = self.medium_line - self.top_bar_height // 2
        self.feature_unlocked_checked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.feature_unlocked_checked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.feature_unlocked_unchecked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.feature_unlocked_unchecked_checkbox_button.y_margin = self.medium_line - self.top_bar_height // 2
        self.feature_unlocked_unchecked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.feature_unlocked_unchecked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.construction_completed_checked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.construction_completed_checked_checkbox_button.y_margin = self.medium_line \
                                                                       - int(7 * self.top_bar_height / 4)
        self.construction_completed_checked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.construction_completed_checked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.construction_completed_unchecked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.construction_completed_unchecked_checkbox_button.y_margin = self.medium_line \
                                                                         - int(7 * self.top_bar_height / 4)
        self.construction_completed_unchecked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.construction_completed_unchecked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.enough_money_checked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.enough_money_checked_checkbox_button.y_margin = self.medium_line - 3 * self.top_bar_height
        self.enough_money_checked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.enough_money_checked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
        self.enough_money_unchecked_checkbox_button.x_margin \
            = self.screen_resolution[0] // 2 + self.bottom_bar_height
        self.enough_money_unchecked_checkbox_button.y_margin = self.medium_line - 3 * self.top_bar_height
        self.enough_money_unchecked_checkbox_button\
            .on_size_changed((self.top_bar_height, self.top_bar_height),
                             int(self.enough_money_unchecked_checkbox_button.base_font_size_property
                                 * self.top_bar_height))
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
        if self.available_windowed_resolutions_position > 0:
            self.decrement_windowed_resolution_button.on_activate()
        else:
            self.decrement_windowed_resolution_button.on_deactivate()

        if self.available_windowed_resolutions_position < len(self.available_windowed_resolutions) - 1:
            self.increment_windowed_resolution_button.on_activate()
        else:
            self.increment_windowed_resolution_button.on_deactivate()

        self.temp_windowed_resolution_label.text = 'x'.join(str(t) for t in self.temp_windowed_resolution)

    def on_change_temp_notification_flags(self, level_up, feature_unlocked, construction_completed, enough_money):
        """
        Updates temp notification flags.
        Activates corresponding checkbox buttons.

        :param level_up:                        flag value for level up notification
        :param feature_unlocked:                flag value for feature unlocked notification
        :param construction_completed:          flag value for construction completed notification
        :param enough_money:                    flag value for enough money notification
        """
        self.temp_level_up_notification_enabled = level_up
        if self.temp_level_up_notification_enabled:
            self.level_up_checked_checkbox_button.on_activate()
        else:
            self.level_up_unchecked_checkbox_button.on_activate()

        self.temp_feature_unlocked_notification_enabled = feature_unlocked
        if self.temp_feature_unlocked_notification_enabled:
            self.feature_unlocked_checked_checkbox_button.on_activate()
        else:
            self.feature_unlocked_unchecked_checkbox_button.on_activate()

        self.temp_construction_completed_notification_enabled = construction_completed
        if self.temp_construction_completed_notification_enabled:
            self.construction_completed_checked_checkbox_button.on_activate()
        else:
            self.construction_completed_unchecked_checkbox_button.on_activate()

        self.temp_enough_money_notification_enabled = enough_money
        if self.temp_enough_money_notification_enabled:
            self.enough_money_checked_checkbox_button.on_activate()
        else:
            self.enough_money_unchecked_checkbox_button.on_activate()

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.windowed_resolution_description_label.text \
                = I18N_RESOURCES['windowed_resolution_description_string'][self.current_locale]
