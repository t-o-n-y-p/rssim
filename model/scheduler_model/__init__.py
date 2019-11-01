from random import choice
from operator import itemgetter
from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, BASE_SCHEDULE


class SchedulerModel(GameBaseModel):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, logger=getLogger(f'root.app.game.map.{map_id}.scheduler.model'))
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks, unlocked_environment, supported_cars_min 
                                  FROM map_progress WHERE map_id = ?''',
                               (self.map_id, ))
        self.unlocked_tracks, self.unlocked_environment, self.supported_cars_min = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                    cars_min, cars_max, switch_direction_required FROM schedule_options 
                                    WHERE min_level <= ? AND max_level >= ? AND map_id = ?''',
                                 (self.level, self.level, self.map_id))
        self.schedule_options = CONFIG_DB_CURSOR.fetchall()
        self.base_schedule = BASE_SCHEDULE[self.map_id]
        USER_DB_CURSOR.execute('''SELECT train_counter, next_cycle_start_time FROM scheduler WHERE map_id = ?''',
                               (self.map_id, ))
        self.train_counter, self.next_cycle_start_time = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT entry_busy_state FROM scheduler WHERE map_id = ?''', (self.map_id, ))
        self.entry_busy_state = list(map(bool, list(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))))
        CONFIG_DB_CURSOR.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                    FROM map_config WHERE level = ? AND map_id = ?''', (self.level, self.map_id))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = CONFIG_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT entry_locked_state FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.entry_locked_state = list(map(bool, list(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))))

    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, 
                                  entry_busy_state = ? WHERE map_id = ?''',
                               (self.train_counter, self.next_cycle_start_time,
                                ','.join(list(map(str, list(map(int, self.entry_busy_state))))), self.map_id))
        USER_DB_CURSOR.execute('''UPDATE map_progress SET entry_locked_state = ?, supported_cars_min = ? 
                                  WHERE map_id = ?''',
                               (','.join(list(map(str, list(map(int, self.entry_locked_state))))),
                                self.supported_cars_min, self.map_id))
        USER_DB_CURSOR.execute('''DELETE FROM base_schedule WHERE map_id = ?''', (self.map_id, ))
        for train in self.base_schedule:
            USER_DB_CURSOR.execute('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                   (self.map_id, *train))

    def on_update_time(self):
        super().on_update_time()
        # new schedule cycle is created if current schedule end is less than schedule cycle length ahead
        if self.game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            # trains are added one by one if both direction and new direction are unlocked by user,
            # otherwise train is skipped
            for i in self.schedule_options:
                if not self.entry_locked_state[i[DIRECTION]] and not self.entry_locked_state[i[NEW_DIRECTION]]:
                    cars = choice([i[CARS_MIN], i[CARS_MAX]])
                    train_options = (self.train_counter, self.next_cycle_start_time
                                     + choice(list(range(i[ARRIVAL_TIME_MIN], i[ARRIVAL_TIME_MAX]))),
                                     i[DIRECTION], i[NEW_DIRECTION], cars, self.frame_per_car * cars,
                                     self.exp_per_car * cars, self.money_per_car * cars, i[SWITCH_DIRECTION_FLAG])
                    self.base_schedule.append(train_options)
                    self.train_counter = (self.train_counter + 1) % TRAIN_ID_LIMIT

            self.next_cycle_start_time += self.schedule_cycle_length
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(ARRIVAL_TIME))
            self.view.base_schedule = self.base_schedule

        # notify Map controller about new train available if arrival time is less or equal than current time
        # and corresponding entry is not busy; only one train at a time is created
        for i in self.base_schedule:
            if self.game_time >= i[ARRIVAL_TIME]:
                if not self.entry_busy_state[i[DIRECTION]]:
                    self.entry_busy_state[i[DIRECTION]] = True
                    if i[CARS] < self.supported_cars_min:
                        state = 'approaching_pass_through'
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK_ID[self.map_id][i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[self.map_id][i[DIRECTION]], state, i[DIRECTION],
                                             i[DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, PASS_THROUGH_BOARDING_TIME,
                                             0.0, 0.0, False)
                    else:
                        state = 'approaching'
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK_ID[self.map_id][i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[self.map_id][i[DIRECTION]], state, i[DIRECTION],
                                             i[NEW_DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, i[STOP_TIME],
                                             i[EXP], i[MONEY], bool(i[SWITCH_DIRECTION_REQUIRED]))

                    index = self.base_schedule.index(i)
                    self.view.on_release_train(index)
                    self.base_schedule.remove(i)
                    break
            else:
                # no more trains can be created because schedule is sorted by arrival time,
                # and arrival time for all following trans will be greater than current time
                break

    def on_level_up(self):
        super().on_level_up()
        CONFIG_DB_CURSOR.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                    cars_min, cars_max FROM schedule_options 
                                    WHERE min_level <= ? AND max_level >= ? AND map_id = ?''',
                                 (self.level, self.level, self.map_id))
        self.schedule_options = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                    FROM map_config WHERE level = ? AND map_id = ?''', (self.level, self.map_id))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = CONFIG_DB_CURSOR.fetchone()

    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        directions_to_unlock = [direction_id for direction_id, (track, environment)
                                in enumerate(MAP_ENTRY_UNLOCK_CONDITIONS[self.map_id])
                                if track == self.unlocked_tracks and environment <= self.unlocked_environment]
        for d in directions_to_unlock:
            self.entry_locked_state[d] = False

        CONFIG_DB_CURSOR.execute('''SELECT supported_cars_min FROM track_config 
                                    WHERE track_number = ? AND map_id = ?''', (track, self.map_id))
        self.supported_cars_min = CONFIG_DB_CURSOR.fetchone()[0]

    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        directions_to_unlock = [direction_id for direction_id, (track, environment)
                                in enumerate(MAP_ENTRY_UNLOCK_CONDITIONS[self.map_id])
                                if track <= self.unlocked_tracks and environment == self.unlocked_environment]
        for d in directions_to_unlock:
            self.entry_locked_state[d] = False

    def on_leave_entry(self, entry_id):
        self.entry_busy_state[entry_id] = False
