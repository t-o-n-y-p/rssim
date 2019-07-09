from ctypes import windll
from logging import getLogger

from model import *


class AppModel(Model):
    def __init__(self):
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
        self.view.on_activate()
        if self.fullscreen_mode:
            self.view.restore_button.on_activate()
        elif self.fullscreen_mode_available:
            self.view.fullscreen_button.on_activate()

    @fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        self.view.on_fullscreen_mode_turned_on()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_ON)

    def on_fullscreen_mode_turned_off(self):
        self.view.on_fullscreen_mode_turned_off()
        self.on_save_and_commit_state(FULLSCREEN_MODE_TURNED_OFF)

    def on_save_and_commit_state(self, fullscreen_mode):
        self.fullscreen_mode = bool(fullscreen_mode)
        self.user_db_cursor.execute('UPDATE graphics SET fullscreen = ?', (fullscreen_mode, ))
        self.user_db_connection.commit()

    def on_save_and_commit_locale(self, new_locale):
        self.user_db_cursor.execute('UPDATE i18n SET current_locale = ?', (new_locale, ))
        self.user_db_connection.commit()

    def on_save_and_commit_clock_state(self, clock_24h_enabled):
        self.user_db_cursor.execute('UPDATE i18n SET clock_24h = ?', (int(clock_24h_enabled), ))
        self.user_db_connection.commit()
