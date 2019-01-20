from ctypes import windll

from model import *


class AppModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.fullscreen_mode_available = False
        if (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()
        self.view.fullscreen_button.on_activate()

    @fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        self.view.on_fullscreen_mode_turned_on()
        self.on_save_and_commit_state(1)

    def on_fullscreen_mode_turned_off(self):
        self.view.on_fullscreen_mode_turned_off()
        self.on_save_and_commit_state(0)

    def on_change_screen_resolution(self, screen_resolution, fullscreen_mode):
        if fullscreen_mode and not self.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_off()

        self.view.on_change_screen_resolution(screen_resolution, fullscreen=fullscreen_mode)

    def on_save_and_commit_state(self, fullscreen_mode):
        self.user_db_cursor.execute('UPDATE graphics_config SET fullscreen = ?', (fullscreen_mode, ))
        self.user_db_connection.commit()
