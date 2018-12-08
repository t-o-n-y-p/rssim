from .model_base import Model


class FPSModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.fps = 0

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view

    def on_update_fps(self, fps):
        self.fps = fps
        self.view.on_update_fps(fps)
