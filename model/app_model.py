from ctypes import windll

from .model_base import Model


def _fullscreen_mode_available(fn):
    def _turn_fullscren_mode_on_if_available(*args, **kwargs):
        if args[0].fullscreen_mode_available:
            fn(*args, **kwargs)

    return _turn_fullscren_mode_on_if_available


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


class AppModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.config_db_cursor.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = self.config_db_cursor.fetchall()
        self.fullscreen_mode_available = False
        if (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()
        self.view.fullscreen_button.on_activate()

    @_fullscreen_mode_available
    def on_fullscreen_mode_turned_on(self):
        self.view.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.view.on_fullscreen_mode_turned_off()

    def on_change_screen_resolution(self, screen_resolution, fullscreen_mode):
        if fullscreen_mode and not self.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_off()

        self.view.on_change_screen_resolution(screen_resolution, fullscreen=fullscreen_mode)
