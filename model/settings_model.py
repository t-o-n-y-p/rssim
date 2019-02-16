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
            available_windowed_resolutions      list of screen resolutions user can select as windowed resolution
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
        self.logger.info('START INIT')
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.logger.debug(f'windowed_resolution: {self.windowed_resolution}')
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics')
        self.fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.logger.debug(f'fullscreen_mode: {self.fullscreen_mode}')
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.logger.debug(f'screen_resolution_config: {self.screen_resolution_config}')
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
        self.logger.debug(f'available_windowed_resolutions: {self.available_windowed_resolutions}')
        self.user_db_cursor.execute('SELECT log_level FROM log_options')
        self.log_level = self.user_db_cursor.fetchone()[0]
        self.logger.debug(f'log_level: {self.log_level}')
        self.fullscreen_mode_available = False
        self.logger.debug(f'fullscreen_mode_available: {self.fullscreen_mode_available}')
        self.fullscreen_resolution = (0, 0)
        self.screen_resolution = (0, 0)
        if (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True
            self.logger.debug(f'fullscreen_mode_available: {self.fullscreen_mode_available}')
            self.fullscreen_resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
            self.logger.debug(f'fullscreen_resolution: {self.fullscreen_resolution}')

        if self.fullscreen_mode and self.fullscreen_mode_available:
            self.screen_resolution = self.fullscreen_resolution
        else:
            self.screen_resolution = self.windowed_resolution

        self.logger.debug(f'screen_resolution: {self.screen_resolution}')
        self.logger.info('END INIT')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.on_activate_view()
        self.logger.info('END ON_ACTIVATE')

    def on_activate_view(self):
        """
        Activates the Settings view, updates temp values for log level, windowed resolution
        and updates available windowed resolutions.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_activate()
        self.view.on_change_temp_log_level(self.log_level)
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)
        self.view.on_change_available_windowed_resolutions(self.available_windowed_resolutions)
        self.logger.info('END ON_ACTIVATE_VIEW')

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution value. Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.screen_resolution = screen_resolution
        self.logger.debug(f'screen_resolution: {self.screen_resolution}')
        self.view.on_change_screen_resolution(self.screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_save_and_commit_state(self):
        """
        Saves user-defined settings to user progress database and makes commit.
        """
        self.logger.info('START ON_SAVE_AND_COMMIT_STATE')
        self.log_level = self.view.temp_log_level
        self.logger.debug(f'log_level: {self.log_level}')
        self.controller.parent_controller.on_save_log_level(self.log_level)
        self.windowed_resolution = self.view.temp_windowed_resolution
        self.logger.debug(f'windowed_resolution: {self.windowed_resolution}')
        self.logger.debug(f'fullscreen: {self.view.surface.fullscreen}')
        if not self.view.surface.fullscreen:
            self.controller.parent_controller.on_change_screen_resolution(self.windowed_resolution, False)

        self.user_db_cursor.execute('UPDATE graphics SET app_width = ?, app_height = ?', self.windowed_resolution)
        self.logger.debug('windowed resolution saved successfully')
        self.user_db_connection.commit()
        self.logger.debug('made commit successfully')
        self.logger.info('END ON_SAVE_AND_COMMIT_STATE')
