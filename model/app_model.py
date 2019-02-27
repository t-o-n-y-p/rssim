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
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        if monitor_resolution_config in self.screen_resolution_config:
            self.fullscreen_mode_available = True
        else:
            self.fullscreen_mode_available = False

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_activate_view(self):
        """
        Activates the App view and appropriate button depending on app window mode.
        """
        self.view.on_activate()
        if self.controller.settings.model.fullscreen_mode:
            self.view.restore_button.on_activate()
        else:
            self.view.fullscreen_button.on_activate()

    @fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        """
        Notifies the view to turn on the fullscreen mode for surface.
        Note that adjusting base offset and content resolution is made by other handlers,
        this one just switches app window mode.
        """
        self.view.on_fullscreen_mode_turned_on()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_ON)

    def on_fullscreen_mode_turned_off(self):
        """
        Notifies the view to turn off the fullscreen mode for surface.
        Note that adjusting base offset and content resolution is made by other handlers,
        this one just switches app window mode.
        """
        self.view.on_fullscreen_mode_turned_off()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_OFF)

    def on_save_and_commit_state(self, fullscreen_mode):
        """
        Saves and commits new fullscreen mode flag value to the user progress database.

        :param fullscreen_mode:                 fullscreen mode flag value to be saved
        """
        self.user_db_cursor.execute('UPDATE graphics SET fullscreen = ?', (fullscreen_mode, ))
        self.user_db_connection.commit()
