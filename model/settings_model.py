from .model_base import Model


class SettingsModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.screen_resolution = (1280, 720)

    def on_activate(self):
        self.is_activated = True
        self.view.on_activate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.view.on_change_screen_resolution(self.screen_resolution)
