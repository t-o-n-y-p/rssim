from win32api import GetSystemMetrics

from .model_base import Model


class AppModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics_config')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics_config')
        self.fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.fullscreen_mode_available = False
        self.fullscreen_resolution = (0, 0)
        self.screen_resolution = (0, 0)
        if (GetSystemMetrics(0), GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True
            self.fullscreen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))

        if self.fullscreen_mode and self.fullscreen_mode_available:
            self.screen_resolution = self.fullscreen_resolution
        else:
            self.screen_resolution = self.windowed_resolution

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view
        if self.fullscreen_mode:
            self.view.restore_button.on_activate()
        else:
            self.view.fullscreen_button.on_activate()

    def on_fullscreen_mode_turned_on(self):
        self.fullscreen_mode = True
        self.save_state()
        self.view.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.fullscreen_mode = False
        self.save_state()
        self.view.on_fullscreen_mode_turned_off()

    def on_change_screen_resolution(self, screen_resolution, fullscreen_mode):
        self.screen_resolution = screen_resolution
        if fullscreen_mode and not self.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_off()

        self.view.on_change_screen_resolution(self.screen_resolution, fullscreen=fullscreen_mode)

    def save_state(self):
        if self.fullscreen_mode:
            self.user_db_cursor.execute('UPDATE graphics_config SET fullscreen = 1')
        else:
            self.user_db_cursor.execute('UPDATE graphics_config SET fullscreen = 0')

        self.user_db_connection.commit()
