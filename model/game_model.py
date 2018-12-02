from .model_base import Model


class GameModel(Model):
    def __init__(self, user_db_connection, user_db_cursor):
        super().__init__(user_db_connection, user_db_cursor)
        self.screen_resolution = (1280, 720)
        self.game_paused = False

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.view.on_change_screen_resolution(self.screen_resolution)

    def on_pause_game(self):
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        self.game_paused = False
        self.view.on_resume_game()
