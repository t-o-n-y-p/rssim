from ctypes import windll
from logging import getLogger

from model import *


class AppModel(Model):
    """
    Implements App model.
    App object is responsible for high-level properties, UI and events.
    """
    def __init__(self):
        """
        Properties:
            fullscreen_mode                     indicates if fullscreen mode is turned on
            screen_resolution_config            app window width and height from user progress database
            fullscreen_mode_available           determines if app supports current monitor resolution
            fullscreen_resolution               app window resolution for fullscreen mode

        """
        super().__init__(logger=getLogger('root.app.model'))
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics')
        self.fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        if monitor_resolution_config in self.screen_resolution_config:
            self.fullscreen_mode_available = True
            self.fullscreen_resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        else:
            self.fullscreen_mode_available = False

    def on_activate_view(self):
        """
        Activates the App view and appropriate button depending on app window mode.
        """
        self.view.on_activate()
        if self.fullscreen_mode:
            self.view.restore_button.on_activate()
        elif self.fullscreen_mode_available:
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
        self.fullscreen_mode = bool(fullscreen_mode)
        self.user_db_cursor.execute('UPDATE graphics SET fullscreen = ?', (fullscreen_mode, ))
        self.user_db_connection.commit()

    def on_save_and_commit_locale(self, new_locale):
        """
        Saves and commits new locale value to the user progress database.

        :param new_locale:                      new value for current locale
        """
        self.user_db_cursor.execute('UPDATE i18n SET current_locale = ?', (new_locale, ))
        self.user_db_connection.commit()

    def on_save_and_commit_clock_state(self, clock_24h_enabled):
        """
        Saves and commits new clock state value to the user progress database.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.user_db_cursor.execute('UPDATE i18n SET clock_24h = ?', (int(clock_24h_enabled), ))
        self.user_db_connection.commit()
