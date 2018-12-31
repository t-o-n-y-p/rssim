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
        self.trains = []
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
        self.entry_train_route = ('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry')
        self.exit_train_route = ('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit')
        self.approaching_train_route = ('left_approaching', 'right_approaching',
                                        'left_side_approaching', 'right_side_approaching')
        self.supported_cars = [0, 0]
        self.user_db_cursor.execute('''SELECT unlocked_tracks, supported_cars_min, supported_cars_max 
                                       FROM game_progress''')
        self.unlocked_tracks, self.supported_cars[0], self.supported_cars[1] = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT busy FROM tracks')
        self.track_busy_status = [None, ]
        busy_status_parsed = self.user_db_cursor.fetchall()
        for i in busy_status_parsed:
            self.track_busy_status.append(bool(i[0]))

        self.supported_cars_by_track = [None, ]
        self.config_db_cursor.execute('SELECT supported_cars_min, supported_cars_max FROM track_config')
        self.supported_cars_by_track.extend(self.config_db_cursor.fetchall())

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        for i in self.trains:
            track_priority_list = None
            if i.model.state == 'approaching':
                track_priority_list = self.main_priority_tracks[i.model.direction][i.model.new_direction]
            elif i.model.state == 'approaching_pass_through':
                track_priority_list = self.pass_through_priority_tracks[i.model.direction]

            for track in track_priority_list:
                if track <= self.unlocked_tracks and not self.track_busy_status[track] \
                        and i.model.cars in range(self.supported_cars_by_track[track][0],
                                                  self.supported_cars_by_track[track][1] + 1):
                    self.track_busy_status[track] = True
                    i.model.state = 'pending_boarding'
                    self.controller.parent_controller.on_close_train_route(i.model.track, i.model.train_route)
                    i.model.track = track
                    i.model.train_route = self.entry_train_route[i.model.direction]
                    self.controller.parent_controller.on_open_train_route(track,
                                                                          self.entry_train_route[i.model.direction],
                                                                          i.train_id, i.model.cars)
                    self.trains.remove(i)

    def on_save_state(self):
        for i in range(1, len(self.track_busy_status)):
            self.user_db_cursor.execute('''UPDATE tracks SET busy = ? WHERE track_number = ?''',
                                        (int(self.track_busy_status[i]), i))

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number

    def on_add_train(self, train_controller):
        self.trains.append(train_controller)

    def on_leave_track(self, track):
        self.track_busy_status[track] = False
