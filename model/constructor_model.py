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


class ConstructorModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.unlock_tracks_matrix = ([], [], [], [], [], [], [], [], [], [5, 6],
                                     [], [], [], [], [], [], [], [], [], [7, 8],
                                     [], [], [], [], [], [], [], [], [], [9, 10],
                                     [], [], [], [], [], [], [], [], [], [11, 12],
                                     [], [], [], [], [], [], [], [], [], [13, 14],
                                     [], [], [], [], [15, 16], [], [], [], [], [17, 18],
                                     [], [], [], [], [19, 20], [], [], [], [], [21, ],
                                     [], [], [], [], [22, ], [], [], [], [], [23, 24],
                                     [], [], [], [], [25, 26], [], [], [], [], [27, 28],
                                     [], [], [], [], [29, 30], [], [], [], [], [31, 32], [])
        self.user_db_cursor.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_track, 
                                       unlock_condition_from_environment, unlock_available FROM tracks 
                                       WHERE locked = 1''')
        self.track_state_matrix = {}
        track_info_fetched = self.user_db_cursor.fetchall()
        for info in track_info_fetched:
            self.track_state_matrix[info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]), bool(info[5]),
                                                bool(info[6]), bool(info[7])]
            self.config_db_cursor.execute('SELECT price FROM track_config WHERE track = ?', (info[0], ))
            self.track_state_matrix[info[0]].append(self.config_db_cursor.fetchone()[0])

        self.track_state_locked = 0
        self.track_state_under_construction = 1
        self.track_state_construction_time = 2
        self.track_state_unlock_condition_from_level = 3
        self.track_state_unlock_condition_from_previous_track = 4
        self.track_state_unlock_condition_from_environment = 5
        self.track_state_unlock_available = 6
        self.track_state_price = 7

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        for track in self.track_state_matrix:
            if self.track_state_matrix[track][self.track_state_under_construction]:
                self.track_state_matrix[track][self.track_state_construction_time] -= 1
                if self.track_state_matrix[track][self.track_state_construction_time] == 0:
                    self.track_state_matrix[track][self.track_state_under_construction] = False
                    self.track_state_matrix[track][self.track_state_locked] = False
                    self.controller.parent_controller.on_unlock_track(track)
                    self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_previous_track] = True
                    if self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_level] \
                            and self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_environment]:
                        self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_previous_track] \
                            = False
                        self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_level] = False
                        self.track_state_matrix[track + 1][self.track_state_unlock_condition_from_environment] = False
                        self.track_state_matrix[track + 1][self.track_state_unlock_available] = True

    def on_save_state(self):
        unlocked_tracks = []
        for track in self.track_state_matrix:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = ?, under_construction = ?, construction_time = ?, 
                                           unlock_condition_from_level = ?, unlock_condition_from_previous_track = ?, 
                                           unlock_condition_from_environment = ?, unlock_available = ? 
                                           WHERE track_number = ?''',
                                        (self.track_state_matrix[track][self.track_state_locked],
                                         self.track_state_matrix[track][self.track_state_under_construction],
                                         self.track_state_matrix[track][self.track_state_construction_time],
                                         self.track_state_matrix[track][self.track_state_unlock_condition_from_level],
                                         self.track_state_matrix[track][
                                             self.track_state_unlock_condition_from_previous_track],
                                         self.track_state_matrix[track][
                                             self.track_state_unlock_condition_from_environment],
                                         self.track_state_matrix[track][self.track_state_unlock_available], track)
                                        )
            if not self.track_state_matrix[track][self.track_state_locked]:
                unlocked_tracks.append(track)

        for track in unlocked_tracks:
            self.track_state_matrix.pop(track)

    def on_level_up(self, level):
        for track in self.unlock_tracks_matrix[level]:
            self.track_state_matrix[track][self.track_state_unlock_condition_from_level] = True
            if self.track_state_matrix[track][self.track_state_unlock_condition_from_previous_track] \
                    and self.track_state_matrix[track][self.track_state_unlock_condition_from_environment]:
                self.track_state_matrix[track][self.track_state_unlock_condition_from_level] = False
                self.track_state_matrix[track][self.track_state_unlock_condition_from_previous_track] = False
                self.track_state_matrix[track][self.track_state_unlock_condition_from_environment] = False
                self.track_state_matrix[track][self.track_state_unlock_available] = True

    def on_put_track_under_construction(self, track):
        self.track_state_matrix[track][self.track_state_unlock_available] = False
        self.track_state_matrix[track][self.track_state_under_construction] = True
