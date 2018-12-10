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
        self.tracks = ()
        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3
        self.user_db_cursor.execute('SELECT level FROM game_progress')
        self.level = self.user_db_cursor.fetchone()[0]
        self.config_db_cursor.execute('''SELECT * FROM (SELECT schedule_options_table_name FROM player_progress_config 
                                      WHERE level = ?)''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.user_db_cursor.execute('SELECT * FROM base_schedule')
        self.base_schedule = self.user_db_cursor.fetchall()
        self.user_db_cursor.execute('SELECT * FROM scheduler')
        self.train_counter, self.next_cycle_start_time = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        if game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            for i in self.schedule_options:
                if i[2] in (self.direction_from_left_to_right, self.direction_from_right_to_left) \
                        or (i[2] == self.direction_from_left_to_right_side and not self.tracks[21].locked)\
                        or (i[2] == self.direction_from_right_to_left_side and not self.tracks[22].locked):
                    cars = choice([i[4], i[5]])
                    self.base_schedule.append(
                        (self.train_counter, self.next_cycle_start_time + choice(list(range(i[0], i[1]))),
                         i[2], i[3], cars, self.frame_per_car * cars, self.exp_per_car * cars,
                         self.money_per_car * cars)
                    )
                    self.train_counter = (self.train_counter + 1) % 1000000

            self.next_cycle_start_time += self.schedule_cycle_length
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(1))

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?',
                                    (self.train_counter, self.next_cycle_start_time))
        self.user_db_cursor.execute('DELETE FROM base_schedule')
        self.user_db_cursor.executemany('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.base_schedule)

    def on_level_up(self):
        self.level += 1
        self.config_db_cursor.execute('''SELECT * FROM (SELECT schedule_options_table_name FROM player_progress_config 
                                      WHERE level = ?)''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()
