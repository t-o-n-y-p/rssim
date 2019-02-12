from random import choice
from operator import itemgetter
from logging import getLogger

from model import *


class SchedulerModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.scheduler.model'))
        self.user_db_cursor.execute('SELECT level, unlocked_tracks, supported_cars_min FROM game_progress')
        self.level, self.unlocked_tracks, self.supported_cars_min = self.user_db_cursor.fetchone()
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

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        if game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            for i in self.schedule_options:
                if (i[DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)
                        and i[NEW_DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)) \
                        or ((i[DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE)
                            and self.unlocked_tracks >= 21)\
                        or ((i[DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE)
                            and self.unlocked_tracks >= 22):
                    cars = choice([i[CARS_MIN], i[CARS_MAX]])
                    self.base_schedule.append(
                        (self.train_counter, self.next_cycle_start_time
                         + choice(list(range(i[ARRIVAL_TIME_MIN], i[ARRIVAL_TIME_MAX]))),
                         i[DIRECTION], i[NEW_DIRECTION], cars, self.frame_per_car * cars,
                         self.exp_per_car * cars, self.money_per_car * cars)
                    )
                    self.train_counter = (self.train_counter + 1) % 1000000

            self.next_cycle_start_time += self.schedule_cycle_length
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(ARRIVAL_TIME))

        self.view.on_update_train_labels(self.base_schedule, game_time)
        for i in self.base_schedule:
            if game_time >= i[ARRIVAL_TIME]:
                if not self.entry_busy_state[i[DIRECTION]]:
                    self.entry_busy_state[i[DIRECTION]] = True
                    if i[CARS] < self.supported_cars_min:
                        state = 'approaching_pass_through'
                        self.controller.parent_controller.on_create_train(i[TRAIN_ID], i[CARS],
                                                                          ENTRY_TRACK[i[DIRECTION]],
                                                                          APPROACHING_TRAIN_ROUTE[i[DIRECTION]],
                                                                          state, i[DIRECTION],
                                                                          i[DIRECTION], i[DIRECTION],
                                                                          10000000, 480, 0.0, 0.0)
                    else:
                        state = 'approaching'
                        self.controller.parent_controller.on_create_train(i[TRAIN_ID], i[CARS],
                                                                          ENTRY_TRACK[i[DIRECTION]],
                                                                          APPROACHING_TRAIN_ROUTE[i[DIRECTION]],
                                                                          state, i[DIRECTION],
                                                                          i[NEW_DIRECTION], i[DIRECTION],
                                                                          10000000, i[STOP_TIME],
                                                                          i[EXP], i[MONEY])
                    index = self.base_schedule.index(i)
                    self.base_schedule.remove(i)
                    self.view.on_release_train(index)
                else:
                    break
            else:
                break

    def on_save_state(self):
        entry_busy_state_string = '{},{},{},{}'.format(int(self.entry_busy_state[0]), int(self.entry_busy_state[1]),
                                                       int(self.entry_busy_state[2]), int(self.entry_busy_state[3]))
        self.user_db_cursor.execute('''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, 
                                       entry_busy_state = ?''',
                                    (self.train_counter, self.next_cycle_start_time, entry_busy_state_string))
        self.user_db_cursor.execute('DELETE FROM base_schedule')
        self.user_db_cursor.executemany('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.base_schedule)
        self.user_db_cursor.execute('UPDATE game_progress SET supported_cars_min = ?', (self.supported_cars_min, ))

    def on_level_up(self, level):
        self.level = level
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
        self.config_db_cursor.execute('SELECT supported_cars_min FROM track_config WHERE track_number = ?',
                                      (track_number, ))
        self.supported_cars_min = self.config_db_cursor.fetchone()[0]

    def on_leave_entry(self, entry_id):
        self.entry_busy_state[entry_id] = False
