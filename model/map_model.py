from .model_base import Model


class MapModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]

    def on_activate(self):
        self.is_activated = True

    def on_deactivate(self):
        self.is_activated = False

    def on_assign_view(self, view):
        self.view = view
        self.view.on_unlock_track(self.unlocked_tracks)

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
        self.view.on_unlock_track(track_number)

    def on_pause_game(self):
        self.game_paused = True

    def on_resume_game(self):
        self.game_paused = False
