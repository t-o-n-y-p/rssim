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


class SchedulerModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3
        self.options_arrival_time_min = 0
        self.options_arrival_time_max = 1
        self.options_direction = 2
        self.options_new_direction = 3
        self.options_cars_min = 4
        self.options_cars_max = 5
        self.base_train_id = 0
        self.base_arrival_time = 1
        self.base_direction = 2
        self.base_new_direction = 3
        self.base_cars = 4
        self.base_stop_time = 5
        self.base_exp = 6
        self.base_money = 7
        self.entry_track = [0, 0, 100, 100]
        self.entry_route = ['left_approaching', 'right_approaching', 'left_side_approaching', 'right_side_approaching']
        self.user_db_cursor.execute('SELECT level, unlocked_tracks FROM game_progress')
        self.level, self.unlocked_tracks = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options WHERE level = ?''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.user_db_cursor.execute('SELECT * FROM base_schedule')
        self.base_schedule = self.user_db_cursor.fetchall()
        self.user_db_cursor.execute('SELECT train_counter, next_cycle_start_time FROM scheduler')
        self.train_counter, self.next_cycle_start_time = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT entry_busy_state FROM scheduler')
        entry_busy_state_parsed = self.user_db_cursor.fetchone()[0].split(',')
        for i in range(len(entry_busy_state_parsed)):
            entry_busy_state_parsed[i] = bool(int(entry_busy_state_parsed[i]))

        self.entry_busy_state = entry_busy_state_parsed
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        if game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            for i in self.schedule_options:
                if i[self.options_direction] in (self.direction_from_left_to_right, self.direction_from_right_to_left) \
                        or (i[self.options_direction] == self.direction_from_left_to_right_side
                            and self.unlocked_tracks >= 21)\
                        or (i[self.options_direction] == self.direction_from_right_to_left_side
                            and self.unlocked_tracks >= 22):
                    cars = choice([i[self.options_cars_min], i[self.options_cars_max]])
                    self.base_schedule.append(
                        (self.train_counter, self.next_cycle_start_time
                         + choice(list(range(i[self.options_arrival_time_min], i[self.options_arrival_time_max]))),
                         i[self.options_direction], i[self.options_new_direction], cars, self.frame_per_car * cars,
                         self.exp_per_car * cars, self.money_per_car * cars)
                    )
                    self.train_counter = (self.train_counter + 1) % 1000000

            self.next_cycle_start_time += self.schedule_cycle_length
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(self.base_arrival_time))

        self.view.on_update_train_labels(self.base_schedule, game_time)
        for i in self.base_schedule:
            if game_time >= i[self.base_arrival_time]:
                if not self.entry_busy_state[i[self.base_direction]]:
                    self.entry_busy_state[i[self.base_direction]] = True
                    self.controller.parent_controller.on_create_train(i[self.base_train_id], i[self.base_cars],
                                                                      self.entry_track[i[self.base_direction]],
                                                                      self.entry_route[i[self.base_direction]],
                                                                      'approaching', i[self.base_direction],
                                                                      i[self.base_new_direction],
                                                                      i[self.base_direction],
                                                                      0, i[self.base_stop_time], i[self.base_exp],
                                                                      i[self.base_money])
                else:
                    break
            else:
                break

    def on_save_state(self):
        entry_busy_state_string = int(self.entry_busy_state[0]) + ',' + int(self.entry_busy_state[1]) + ',' \
                                  + int(self.entry_busy_state[2]) + ',' + int(self.entry_busy_state[3])
        self.user_db_cursor.execute('''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, 
                                       entry_busy_state = ?''',
                                    (self.train_counter, self.next_cycle_start_time, entry_busy_state_string))
        self.user_db_cursor.execute('DELETE FROM base_schedule')
        self.user_db_cursor.executemany('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.base_schedule)

    def on_level_up(self):
        self.level += 1
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options WHERE level = ?''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number

    def on_leave_entry(self, entry_id):
        self.entry_busy_state[entry_id] = False
