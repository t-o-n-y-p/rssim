from random import choice
from operator import itemgetter

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


class DispatcherModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3
        self.main_priority_tracks = (((20, 18, 16, 14, 12, 10, 8, 6, 4),
                                      (20, 18, 16, 14, 12, 10, 8, 6, 4),
                                      (32, 30, 28, 26, 24, 22), (23, 21)),
                                     ((19, 17, 15, 13, 11, 9, 7, 5, 3),
                                      (19, 17, 15, 13, 11, 9, 7, 5, 3),
                                      (24, 22), (31, 29, 27, 25, 23, 21)),
                                     ((31, 29, 27, 25, 23, 21), (23, 21), (0,), (31, 29, 27, 25, 23, 21)),
                                     ((24, 22), (32, 30, 28, 26, 24, 22), (32, 30, 28, 26, 24, 22), (0,)))
        self.pass_through_priority_tracks = ((2, 1), (1, 2))
        self.base_train_id = 0
        self.base_arrival_time = 1
        self.base_direction = 2
        self.base_new_direction = 3
        self.base_cars = 4
        self.base_stop_time = 5
        self.base_exp = 6
        self.base_money = 7
        self.supported_cars = [0, 0]
        self.user_db_cursor.execute('''SELECT unlocked_tracks, supported_carts_min, supported_carts_max 
                                       FROM game_progress''')
        self.unlocked_tracks, self.supported_cars[0], self.supported_cars[1] = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT track_busy_status FROM dispatcher')
        self.track_busy_status = self.user_db_cursor.fetchone()[0].split(',')
        for i in range(len(self.track_busy_status)):
            self.track_busy_status[i] = bool(int(self.track_busy_status[i]))

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        pass

    def on_save_state(self):
        track_busy_status_string = ''
        for i in self.track_busy_status:
            track_busy_status_string += f'{i},'

        track_busy_status_string = track_busy_status_string[0:len(track_busy_status_string) - 1]
        self.user_db_cursor.execute('UPDATE dispatcher SET track_busy_status = ?', (track_busy_status_string, ))

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
