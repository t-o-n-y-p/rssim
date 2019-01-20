from pyglet.text import Label

from view import *
from button.accept_settings_button import AcceptSettingsButton
from button.reject_settings_button import RejectSettingsButton
from button.increment_windowed_resolution_button import IncrementWindowedResolutionButton
from button.decrement_windowed_resolution_button import DecrementWindowedResolutionButton


class SettingsView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        def on_accept_settings(button):
            self.controller.on_save_and_commit_state()
            self.controller.on_deactivate()

        def on_reject_settings(button):
            self.controller.on_deactivate()

        def on_increment_windowed_resolution(button):
            self.available_windowed_resolutions_position += 1
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position]
            )
            if self.available_windowed_resolutions_position == len(self.available_windowed_resolutions) - 1:
                button.on_deactivate()

            self.decrement_windowed_resolution_button.on_activate()

        def on_decrement_windowed_resolution(button):
            self.available_windowed_resolutions_position -= 1
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position]
            )
            if self.available_windowed_resolutions_position == 0:
                button.on_deactivate()

            self.increment_windowed_resolution_button.on_activate()

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups)
        self.temp_windowed_resolution = (0, 0)
        self.temp_log_level = 0
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        self.settings_opacity = 0
        self.temp_fullscreen_mode = False
        self.available_windowed_resolutions = []
        self.available_windowed_resolutions_position = 0
        self.accept_settings_button = AcceptSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_accept_settings)
        self.buttons.append(self.accept_settings_button)
        self.reject_settings_button = RejectSettingsButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_reject_settings)
        self.buttons.append(self.reject_settings_button)
        self.increment_windowed_resolution_button \
            = IncrementWindowedResolutionButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                groups=self.groups, on_click_action=on_increment_windowed_resolution)
        self.decrement_windowed_resolution_button \
            = DecrementWindowedResolutionButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                groups=self.groups, on_click_action=on_decrement_windowed_resolution)
        self.buttons.append(self.increment_windowed_resolution_button)
        self.buttons.append(self.decrement_windowed_resolution_button)
        self.temp_windowed_resolution_label = None
        self.windowed_resolution_description_label = None

    def on_update(self):
        if self.is_activated and self.settings_opacity < 255:
            self.settings_opacity += 15

        if not self.is_activated and self.settings_opacity > 0:
            self.settings_opacity -= 15

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.temp_windowed_resolution_label \
            = Label('{}x{}'.format(self.temp_windowed_resolution[0], self.temp_windowed_resolution[1]),
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line + self.top_bar_height,
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.windowed_resolution_description_label \
            = Label('Game resolution in window mode (not fullscreen):',
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line + self.top_bar_height * 2,
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.temp_windowed_resolution_label.delete()
        self.temp_windowed_resolution_label = None
        self.windowed_resolution_description_label.delete()
        self.windowed_resolution_description_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        if self.is_activated:
            self.temp_windowed_resolution_label.x = self.screen_resolution[0] // 4
            self.temp_windowed_resolution_label.y = self.medium_line + self.top_bar_height
            self.temp_windowed_resolution_label.font_size = int(16 / 80 * self.bottom_bar_height)
            self.windowed_resolution_description_label.x = self.screen_resolution[0] // 4
            self.windowed_resolution_description_label.y = self.medium_line + self.top_bar_height * 2
            self.windowed_resolution_description_label.font_size = int(16 / 80 * self.bottom_bar_height)

        self.accept_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height * 2 + 2
        self.accept_settings_button.y_margin = 0
        self.accept_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                    int(48 / 80 * self.bottom_bar_height))
        self.reject_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.reject_settings_button.y_margin = 0
        self.reject_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                    self.bottom_bar_height // 2)
        self.increment_windowed_resolution_button.x_margin \
            = 11 * self.screen_resolution[0] // 32 - self.top_bar_height // 2
        self.increment_windowed_resolution_button.y_margin = self.medium_line + self.top_bar_height // 2
        self.increment_windowed_resolution_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                                  int(16 / 40 * self.top_bar_height))
        self.decrement_windowed_resolution_button.x_margin \
            = 5 * self.screen_resolution[0] // 32 - self.top_bar_height // 2
        self.decrement_windowed_resolution_button.y_margin = self.medium_line + self.top_bar_height // 2
        self.decrement_windowed_resolution_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                                  int(16 / 40 * self.top_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        self.temp_windowed_resolution = windowed_resolution
        self.temp_windowed_resolution_label.text \
            = '{}x{}'.format(self.temp_windowed_resolution[0], self.temp_windowed_resolution[1])

    def on_change_available_windowed_resolutions(self, available_windowed_resolutions):
        self.available_windowed_resolutions = available_windowed_resolutions
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)
        if self.available_windowed_resolutions_position > 0:
            self.decrement_windowed_resolution_button.on_activate()

        if self.available_windowed_resolutions_position < len(self.available_windowed_resolutions) - 1:
            self.increment_windowed_resolution_button.on_activate()

    def on_change_temp_log_level(self, log_level):
        self.temp_log_level = log_level
