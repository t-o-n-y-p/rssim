from logging import getLogger
from ctypes import windll

from pyglet.text import Label

from view import *
from button.accept_settings_button import AcceptSettingsButton
from button.reject_settings_button import RejectSettingsButton
from button.increment_windowed_resolution_button import IncrementWindowedResolutionButton
from button.decrement_windowed_resolution_button import DecrementWindowedResolutionButton


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
            self.logger.info('START ON_ACCEPT_CHANGES')
            self.controller.on_save_and_commit_state()
            self.controller.on_deactivate()
            self.logger.info('END ON_ACCEPT_CHANGES')

        def on_reject_changes(button):
            """
            Notifies controller that player rejects changes.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_REJECT_CHANGES')
            self.controller.on_deactivate()
            self.logger.info('END ON_REJECT_CHANGES')

        def on_increment_windowed_resolution(button):
            """
            Updates windowed resolution when user increases it.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_INCREMENT_WINDOWED_RESOLUTION')
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position + 1]
            )
            self.logger.info('END ON_INCREMENT_WINDOWED_RESOLUTION')

        def on_decrement_windowed_resolution(button):
            """
            Updates windowed resolution when user decreases it.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_DECREMENT_WINDOWED_RESOLUTION')
            self.on_change_temp_windowed_resolution(
                self.available_windowed_resolutions[self.available_windowed_resolutions_position - 1]
            )
            self.logger.info('END ON_DECREMENT_WINDOWED_RESOLUTION')

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.settings.view'))
        self.logger.info('START INIT')
        self.temp_windowed_resolution = (0, 0)
        self.temp_log_level = 0
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        self.logger.debug(f'medium_line: {self.medium_line}')
        self.settings_opacity = 0
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
        self.logger.debug(f'available_windowed_resolutions: {self.available_windowed_resolutions}')
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
        self.logger.debug('buttons created successfully')
        self.buttons.append(self.increment_windowed_resolution_button)
        self.buttons.append(self.decrement_windowed_resolution_button)
        self.logger.debug(f'buttons list length: {len(self.buttons)}')
        self.temp_windowed_resolution_label = None
        self.windowed_resolution_description_label = None
        self.logger.info('END INIT')

    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE')
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.debug(f'settings_opacity: {self.settings_opacity}')
        if self.is_activated and self.settings_opacity < 255:
            self.settings_opacity += 15
            self.logger.debug(f'settings_opacity: {self.settings_opacity}')

        if not self.is_activated and self.settings_opacity > 0:
            self.settings_opacity -= 15
            self.logger.debug(f'settings_opacity: {self.settings_opacity}')

        self.logger.info('END ON_UPDATE')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.temp_windowed_resolution_label \
            = Label('x'.join(str(t) for t in self.temp_windowed_resolution),
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line + self.top_bar_height,
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.logger.debug(f'temp_windowed_resolution_label text: {self.temp_windowed_resolution_label.text}')
        self.logger.debug('temp_windowed_resolution_label position: {}'
                          .format((self.temp_windowed_resolution_label.x, self.temp_windowed_resolution_label.y)))
        self.logger.debug(f'temp_windowed_resolution_label font size: {self.temp_windowed_resolution_label.font_size}')
        self.windowed_resolution_description_label \
            = Label('Game resolution in window mode (not fullscreen):',
                    font_name='Arial', font_size=int(16 / 80 * self.bottom_bar_height),
                    x=self.screen_resolution[0] // 4, y=self.medium_line + self.top_bar_height * 2,
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.logger.debug(f'windowed_resolution_description_label text: {self.temp_windowed_resolution_label.text}')
        self.logger.debug('windowed_resolution_description_label position: {}'
                          .format((self.windowed_resolution_description_label.x,
                                   self.windowed_resolution_description_label.y)))
        self.logger.debug('windowed_resolution_description_label font size: {}'
                          .format(self.windowed_resolution_description_label.font_size))
        for b in self.buttons:
            self.logger.debug(f'button: {b.__class__.__name__}')
            self.logger.debug(f'to_activate_on_controller_init: {b.to_activate_on_controller_init}')
            if b.to_activate_on_controller_init:
                b.on_activate()

        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.temp_windowed_resolution_label.delete()
        self.temp_windowed_resolution_label = None
        self.logger.debug(f'temp_windowed_resolution_label: {self.temp_windowed_resolution_label}')
        self.windowed_resolution_description_label.delete()
        self.windowed_resolution_description_label = None
        self.logger.debug(f'windowed_resolution_description_label: {self.windowed_resolution_description_label}')
        for b in self.buttons:
            b.on_deactivate()

        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.medium_line = self.screen_resolution[1] // 2 + self.top_bar_height // 2
        self.logger.debug(f'medium_line: {self.medium_line}')
        self.logger.debug(f'is activated: {self.is_activated}')
        if self.is_activated:
            self.temp_windowed_resolution_label.x = self.screen_resolution[0] // 4
            self.temp_windowed_resolution_label.y = self.medium_line + self.top_bar_height
            self.temp_windowed_resolution_label.font_size = int(16 / 80 * self.bottom_bar_height)
            self.logger.debug('temp_windowed_resolution_label position: {}'
                              .format((self.temp_windowed_resolution_label.x, self.temp_windowed_resolution_label.y)))
            self.logger.debug('temp_windowed_resolution_label font size: {}'
                              .format(self.temp_windowed_resolution_label.font_size))
            self.windowed_resolution_description_label.x = self.screen_resolution[0] // 4
            self.windowed_resolution_description_label.y = self.medium_line + self.top_bar_height * 2
            self.windowed_resolution_description_label.font_size = int(16 / 80 * self.bottom_bar_height)
            self.logger.debug('windowed_resolution_description_label position: {}'
                              .format((self.windowed_resolution_description_label.x,
                                       self.windowed_resolution_description_label.y)))
            self.logger.debug('windowed_resolution_description_label font size: {}'
                              .format(self.windowed_resolution_description_label.font_size))

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

        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        """
        Updates temp windowed resolution and text label for it, windowed resolution position.
        Activates and deactivates windowed resolution buttons if needed.

        :param windowed_resolution:             selected windowed resoltion
        """
        self.logger.info('START ON_CHANGE_TEMP_WINDOWED_RESOLUTION')
        self.temp_windowed_resolution = windowed_resolution
        self.logger.debug(f'temp_windowed_resolution: {self.temp_windowed_resolution}')
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)
        self.logger.debug(f'available_windowed_resolutions_position: {self.available_windowed_resolutions_position}')
        self.logger.debug(f'available_windowed_resolutions length: {len(self.available_windowed_resolutions)}')
        if self.available_windowed_resolutions_position > 0:
            self.decrement_windowed_resolution_button.on_activate()
        else:
            self.decrement_windowed_resolution_button.on_deactivate()

        if self.available_windowed_resolutions_position < len(self.available_windowed_resolutions) - 1:
            self.increment_windowed_resolution_button.on_activate()
        else:
            self.increment_windowed_resolution_button.on_deactivate()

        self.temp_windowed_resolution_label.text = 'x'.join(str(t) for t in self.temp_windowed_resolution)
        self.logger.debug(f'temp_windowed_resolution_label text: {self.temp_windowed_resolution_label.text}')
        self.logger.info('END ON_CHANGE_TEMP_WINDOWED_RESOLUTION')

    def on_change_temp_log_level(self, log_level):
        """
        Updates temp log level and text label for it.

        :param log_level:                       selected log level
        """
        self.logger.info('START ON_CHANGE_TEMP_LOG_LEVEL')
        self.temp_log_level = log_level
        self.logger.debug(f'temp_log_level: {self.temp_log_level}')
        self.logger.info('END ON_CHANGE_TEMP_LOG_LEVEL')
