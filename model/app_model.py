from ctypes import windll
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, on_commit, TRUE, FALSE
from model import AppBaseModel, fullscreen_mode_available


@final
class AppModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.model'))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        self.fullscreen_mode = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        if (monitor_resolution_config := (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))) \
                in self.screen_resolution_config:
            self.fullscreen_mode_available = True
            self.fullscreen_resolution = monitor_resolution_config
        else:
            self.fullscreen_mode_available = False

    def on_save_state(self):
        USER_DB_CURSOR.execute('UPDATE graphics SET fullscreen = ?', (self.fullscreen_mode, ))

    @fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        self.fullscreen_mode = TRUE
        self.view.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.fullscreen_mode = FALSE
        self.view.on_fullscreen_mode_turned_off()

    @staticmethod
    def on_save_and_commit_locale(new_locale):
        USER_DB_CURSOR.execute('UPDATE i18n SET current_locale = ?', (new_locale, ))
        on_commit()

    @staticmethod
    def on_save_and_commit_clock_state(clock_24h_enabled):
        USER_DB_CURSOR.execute('UPDATE i18n SET clock_24h = ?', (clock_24h_enabled, ))
        on_commit()

    @staticmethod
    def on_save_and_commit_bonus_code_abuse():
        USER_DB_CURSOR.execute('UPDATE game_progress SET bonus_codes_locked = 1')
        on_commit()
