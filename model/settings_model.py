from logging import getLogger
from ctypes import windll

from model import *


class SettingsModel(Model):
    """
    Implements Settings model.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            display_fps                         indicates if FPS value is displayed in game
            windowed_resolution                 screen resolution in windowed mode
            fullscreen_mode                     indicates if fullscreen mode is enabled by user
            screen_resolution_config            list of all supported app window resolutions
            log_level                           telemetry level
            fullscreen_mode_available           indicates if fullscreen mode is available
            fullscreen_resolution               suggested fullscreen mode resolution base on monitor config
            screen_resolution                   current app window resolution
            level_up_notification_enabled
                                indicates if level up notifications are enabled by user in game settings
            feature_unlocked_notification_enabled
                                indicates if feature unlocked notifications are enabled by user in game settings
            construction_completed_notification_enabled
                                indicates if construction completed notifications are enabled by user in game settings
            enough_money_notification_enabled
                                indicates if enough money notifications are enabled by user in game settings

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.settings.model'))
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT fullscreen, display_fps FROM graphics')
        self.fullscreen_mode, self.display_fps = tuple(map(bool, self.user_db_cursor.fetchone()))
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.fullscreen_mode_available = False
        self.fullscreen_resolution = (0, 0)
        self.screen_resolution = (0, 0)
        if (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True
            self.fullscreen_resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))

        if self.fullscreen_mode and self.fullscreen_mode_available:
            self.screen_resolution = self.fullscreen_resolution
        else:
            self.screen_resolution = self.windowed_resolution

        self.user_db_cursor.execute('SELECT * FROM notification_settings')
        self.level_up_notification_enabled, self.feature_unlocked_notification_enabled, \
            self.construction_completed_notification_enabled, self.enough_money_notification_enabled \
            = tuple(map(bool, self.user_db_cursor.fetchone()))

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        """
        Activates the Settings view, updates temp values for log level, windowed resolution
        and updates available windowed resolutions.
        """
        self.view.on_activate()
        self.view.on_change_temp_display_fps(self.display_fps)
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)
        self.view.on_change_temp_notification_flags(self.level_up_notification_enabled,
                                                    self.feature_unlocked_notification_enabled,
                                                    self.construction_completed_notification_enabled,
                                                    self.enough_money_notification_enabled)

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution value. Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        self.view.on_change_screen_resolution(self.screen_resolution)

    def on_save_and_commit_state(self):
        """
        Notifies the app controller about user-defined settings update.
        Saves user-defined settings to user progress database and makes commit.
        """
        self.display_fps = self.view.temp_display_fps
        self.controller.parent_controller.fps.on_update_display_fps(self.display_fps)
        self.windowed_resolution = self.view.temp_windowed_resolution
        if not self.view.surface.fullscreen:
            self.controller.parent_controller.on_change_screen_resolution(self.windowed_resolution)

        self.level_up_notification_enabled = self.view.temp_level_up_notification_enabled
        self.feature_unlocked_notification_enabled = self.view.temp_feature_unlocked_notification_enabled
        self.construction_completed_notification_enabled = self.view.temp_construction_completed_notification_enabled
        self.enough_money_notification_enabled = self.view.temp_enough_money_notification_enabled
        self.controller.parent_controller.on_change_level_up_notification_state(self.level_up_notification_enabled)
        self.controller.parent_controller\
            .on_change_feature_unlocked_notification_state(self.feature_unlocked_notification_enabled)
        self.controller.parent_controller\
            .on_change_construction_completed_notification_state(self.construction_completed_notification_enabled)
        self.controller.parent_controller\
            .on_change_enough_money_notification_state(self.enough_money_notification_enabled)

        self.user_db_cursor.execute('UPDATE graphics SET app_width = ?, app_height = ?, display_fps = ?',
                                    (self.windowed_resolution[0], self.windowed_resolution[1], int(self.display_fps)))
        self.user_db_cursor.execute('''UPDATE notification_settings SET level_up_notification_enabled = ?, 
                                       feature_unlocked_notification_enabled = ?, 
                                       construction_completed_notification_enabled = ?, 
                                       enough_money_notification_enabled = ?''',
                                    tuple(map(int, (self.level_up_notification_enabled,
                                                    self.feature_unlocked_notification_enabled,
                                                    self.construction_completed_notification_enabled,
                                                    self.enough_money_notification_enabled))))
        self.user_db_connection.commit()
