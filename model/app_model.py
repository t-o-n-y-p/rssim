from .model_base import Model


class AppModel(Model):
    def __init__(self, user_db_connection):
        super().__init__(user_db_connection)
        self.user_db_connection.execute('SELECT app_width, app_height FROM graphics_config')
        self.screen_resolution = self.user_db_connection.fetchone()
        self.user_db_connection.execute('SELECT fullscreen FROM graphics_config')
        self.fullscreen_mode = bool(self.user_db_connection.fetchone()[0])

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view
        self.view.on_change_screen_resolution(self.screen_resolution)

    def on_fullscreen_mode_turned_on(self):
        self.fullscreen_mode = True
        self.view.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.fullscreen_mode = False
        self.view.on_fullscreen_mode_turned_off()
