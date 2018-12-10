from .model_base import Model


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


class MapModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_unlock_track(self.unlocked_tracks)

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
        self.view.on_unlock_track(track_number)

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE game_progress SET unlocked_tracks = ?', (self.unlocked_tracks, ))
