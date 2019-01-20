from ctypes import windll

from model import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class SettingsModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics_config')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT fullscreen FROM graphics_config')
        self.fullscreen_mode = bool(self.user_db_cursor.fetchone()[0])
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT app_width, app_height FROM screen_resolution_config 
                                         WHERE manual_setup = 1 AND app_width <= ?''',
                                      (windll.user32.GetSystemMetrics(0),))
        self.available_windowed_resolutions = self.config_db_cursor.fetchall()
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

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_change_temp_log_level(self.log_level)
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)
        self.view.on_change_available_windowed_resolutions(self.available_windowed_resolutions)

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.view.on_change_screen_resolution(self.screen_resolution)

    def on_save_and_commit_state(self):
        self.log_level = self.view.temp_log_level
        self.controller.parent_controller.on_save_log_level(self.log_level)
        self.windowed_resolution = self.view.temp_windowed_resolution
        if not self.view.surface.fullscreen:
            self.controller.parent_controller.on_change_screen_resolution(self.windowed_resolution, False)

        self.user_db_cursor.execute('UPDATE graphics_config SET app_width = ?, app_height = ?',
                                    self.windowed_resolution)
        self.user_db_connection.commit()
