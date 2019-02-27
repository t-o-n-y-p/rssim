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
            windowed_resolution                 screen resolution in windowed mode
            fullscreen_mode                     indicates if fullscreen mode is enabled by user
            screen_resolution_config            list of all supported app window resolutions
            log_level                           telemetry level
            fullscreen_mode_available           indicates if fullscreen mode is available
            fullscreen_resolution               suggested fullscreen mode resolution base on monitor config
            screen_resolution                   current app window resolution

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.settings.model'))
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics')
        self.fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.user_db_cursor.execute('SELECT log_level FROM log_options')
        self.log_level = self.user_db_cursor.fetchone()[0]
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
        self.view.on_change_temp_log_level(self.log_level)
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)

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
        Saves user-defined settings to user progress database and makes commit.
        """
        self.windowed_resolution = self.view.temp_windowed_resolution
        if not self.view.surface.fullscreen:
            self.controller.parent_controller.on_change_screen_resolution(self.windowed_resolution)

        self.user_db_cursor.execute('UPDATE graphics SET app_width = ?, app_height = ?', self.windowed_resolution)
        self.user_db_connection.commit()
