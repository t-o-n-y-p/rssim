from .model_base import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


class GameModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = self.user_db_cursor.fetchone()[0]

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view
        self.view.on_update_game_time(self.game_time)

    def on_pause_game(self):
        self.game_paused = True
        self.view.on_pause_game()

    def on_resume_game(self):
        self.game_paused = False
        self.view.on_resume_game()

    @_model_is_active
    def on_update(self):
        self.game_time += 1
        if self.game_time % 240 == 0:
            self.view.on_update_game_time(self.game_time)
