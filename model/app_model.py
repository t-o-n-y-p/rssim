from ctypes import windll
from logging import getLogger

from model import *


class AppModel(Model):
    """
    Implements App model.
    App object is responsible for high-level properties, UI and events.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            screen_resolution_config            app window width and height from user progress database
            monitor_resolution_config           current monitor resolution
            fullscreen_mode_available           determines if app supports current monitor resolution

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.model'))
        self.logger.info('START INIT')
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.logger.debug(f'screen_resolution_config: {self.screen_resolution_config}')
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        self.logger.debug(f'monitor_resolution_config: {monitor_resolution_config}')
        if monitor_resolution_config in self.screen_resolution_config:
            self.fullscreen_mode_available = True
        else:
            self.fullscreen_mode_available = False

        self.logger.debug(f'fullscreen_mode_available: {self.fullscreen_mode_available}')
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

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_activate_view(self):
        """
        Activates the App view and appropriate button depending on app window mode.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_activate()
        self.logger.debug(f'fullscreen mode: {self.controller.settings.model.fullscreen_mode}')
        if self.controller.settings.model.fullscreen_mode:
            self.logger.debug('fullscreen mode is enabled, activate restore button')
            self.view.restore_button.on_activate()
        else:
            self.logger.debug('windowed mode is enabled, activate fullscreen button')
            self.view.fullscreen_button.on_activate()

        self.logger.info('END ON_ACTIVATE_VIEW')

    @fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        """
        Notifies the view to turn on the fullscreen mode for surface.
        Note that adjusting base offset and content resolution is made by other handlers,
        this one just switches app window mode.
        """
        self.logger.info('START ON_FULLSCREEN_MODE_TURNED_ON')
        self.view.on_fullscreen_mode_turned_on()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_ON)
        self.logger.info('END ON_FULLSCREEN_MODE_TURNED_ON')

    def on_fullscreen_mode_turned_off(self):
        """
        Notifies the view to turn off the fullscreen mode for surface.
        Note that adjusting base offset and content resolution is made by other handlers,
        this one just switches app window mode.
        """
        self.logger.info('START ON_FULLSCREEN_MODE_TURNED_OFF')
        self.view.on_fullscreen_mode_turned_off()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_OFF)
        self.logger.info('END ON_FULLSCREEN_MODE_TURNED_OFF')

    def on_save_and_commit_state(self, fullscreen_mode):
        """
        Saves and commits new fullscreen mode flag value to the user progress database.

        :param fullscreen_mode:                 fullscreen mode flag value to be saved
        """
        self.logger.info('START ON_SAVE_AND_COMMIT_STATE')
        self.logger.debug(f'fullscreen_mode: {fullscreen_mode}')
        self.user_db_cursor.execute('UPDATE graphics SET fullscreen = ?', (fullscreen_mode, ))
        self.logger.debug('fullscreen mode flag saved successfully')
        self.user_db_connection.commit()
        self.logger.debug('made commit successfully')
        self.logger.info('END ON_SAVE_AND_COMMIT_STATE')
