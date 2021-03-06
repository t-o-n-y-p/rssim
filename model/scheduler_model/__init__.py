from abc import ABC, abstractmethod
from random import choice
from operator import itemgetter
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, BASE_SCHEDULE, TRAIN_ID_POOL, DIRECTION, NEW_DIRECTION, \
    CARS_MIN, CARS_MAX, ARRIVAL_TIME_MIN, ARRIVAL_TIME_MAX, SWITCH_DIRECTION_FLAG, SECONDS_IN_ONE_DAY, ARRIVAL_TIME, \
    TRUE, FALSE, CARS, TRAIN_ID, STOP_TIME, EXP, MONEY, SWITCH_DIRECTION_REQUIRED
from model import MapBaseModel, JOINT_ENTRIES, MAP_ENTRY_UNLOCK_CONDITIONS, ENTRY_TRACK_ID, APPROACHING_TRAIN_ROUTE, \
    DEFAULT_PRIORITY, PASS_THROUGH_BOARDING_TIME


class SchedulerModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.scheduler.model'))
        USER_DB_CURSOR.execute(
            '''SELECT locked, unlocked_tracks, unlocked_environment FROM map_progress WHERE map_id = ?''',
            (self.map_id, )
        )
        self.locked, self.unlocked_tracks, self.unlocked_environment = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute(
            '''SELECT min_supported_cars_by_direction FROM map_progress WHERE map_id = ?''', (self.map_id, )
        )
        self.min_supported_cars_by_direction = [
            [int(c) for c in s.split(',')] for s in USER_DB_CURSOR.fetchone()[0].split('|')
        ]
        CONFIG_DB_CURSOR.execute(
            '''SELECT arrival_time_min, arrival_time_max, direction, new_direction, cars_min, cars_max, 
            switch_direction_required FROM schedule_options WHERE min_level <= ? AND max_level >= ? AND map_id = ?''',
            (self.level, self.level, self.map_id)
        )
        self.schedule_options = CONFIG_DB_CURSOR.fetchall()
        USER_DB_CURSOR.execute(
            '''SELECT next_cycle_start_time FROM scheduler WHERE map_id = ?''', (self.map_id, )
        )
        self.next_cycle_start_time = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('''SELECT entry_busy_state FROM scheduler WHERE map_id = ?''', (self.map_id, ))
        self.entry_busy_state = [int(t) for t in USER_DB_CURSOR.fetchone()[0].split(',')]
        CONFIG_DB_CURSOR.execute(
            '''SELECT schedule_cycle_length, seconds_per_car, exp_per_car, money_per_car 
            FROM map_config WHERE level = ? AND map_id = ?''', (self.level, self.map_id)
        )
        if (schedule_config := CONFIG_DB_CURSOR.fetchone()) is not None:
            self.schedule_cycle_length, self.seconds_per_car, self.exp_per_car, self.money_per_car = schedule_config
        else:
            self.schedule_cycle_length, self.seconds_per_car, self.exp_per_car, self.money_per_car = 0, 0, 0.0, 0.0

        USER_DB_CURSOR.execute('''SELECT entry_locked_state FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.entry_locked_state = [int(t) for t in USER_DB_CURSOR.fetchone()[0].split(',')]
        self.exit_locked_state = self.entry_locked_state.copy()
        for i in range(0, len(self.exit_locked_state), 2):
            self.exit_locked_state[i], self.exit_locked_state[i + 1] \
                = self.exit_locked_state[i + 1], self.exit_locked_state[i]

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute(
            '''UPDATE scheduler SET next_cycle_start_time = ?, entry_busy_state = ? WHERE map_id = ?''',
            (self.next_cycle_start_time, ','.join(str(t) for t in self.entry_busy_state), self.map_id)
        )
        USER_DB_CURSOR.execute(
            '''UPDATE map_progress SET entry_locked_state = ?, min_supported_cars_by_direction = ? WHERE map_id = ?''',
            (
                ','.join(str(t) for t in self.entry_locked_state),
                '|'.join([
                    ','.join(str(c) for c in self.min_supported_cars_by_direction[direction])
                    for direction in range(len(self.min_supported_cars_by_direction))
                ]),
                self.map_id
            )
        )
        USER_DB_CURSOR.execute('''DELETE FROM base_schedule WHERE map_id = ?''', (self.map_id, ))
        for train in BASE_SCHEDULE[self.map_id]:
            USER_DB_CURSOR.execute(
                'INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.map_id, *train)
            )

        for train_id, expiration_time in TRAIN_ID_POOL[self.map_id].items():
            USER_DB_CURSOR.execute(
                '''UPDATE train_numbers SET expiration_time = ? WHERE train_id = ? AND map_id = ?''',
                (expiration_time, train_id, self.map_id)
            )

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        # new schedule cycle is created if current schedule end is less than schedule cycle length ahead
        if not self.locked and self.game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            # trains are added one by one if both direction and new direction are unlocked by user,
            # otherwise train is skipped
            for i in self.schedule_options:
                if not self.entry_locked_state[i[DIRECTION]] and not self.exit_locked_state[i[NEW_DIRECTION]]:
                    cars = choice(list(range(i[CARS_MIN], i[CARS_MAX] + 1)))
                    train_id = choice(
                        [train_id for train_id, expiration_time in TRAIN_ID_POOL[self.map_id].items()
                         if expiration_time <= self.game_time]
                    )
                    train_options = (
                        train_id,
                        self.next_cycle_start_time
                        + choice(list(range(i[ARRIVAL_TIME_MIN], i[ARRIVAL_TIME_MAX]))),
                        i[DIRECTION], i[NEW_DIRECTION], cars, self.seconds_per_car * cars,
                        self.exp_per_car * cars, self.money_per_car * cars, i[SWITCH_DIRECTION_FLAG]
                    )
                    BASE_SCHEDULE[self.map_id].append(train_options)
                    TRAIN_ID_POOL[self.map_id][train_id] = self.game_time + SECONDS_IN_ONE_DAY

            self.next_cycle_start_time += self.schedule_cycle_length
            BASE_SCHEDULE[self.map_id].sort(key=itemgetter(ARRIVAL_TIME))
            # self.view.base_schedule = self.base_schedule

        # notify Map controller about new train available if arrival time is less or equal than current time
        # and corresponding entry is not busy; only one train at a time is created
        for i in BASE_SCHEDULE[self.map_id]:
            if self.game_time >= i[ARRIVAL_TIME]:
                if not self.entry_busy_state[i[DIRECTION]]:
                    self.entry_busy_state[i[DIRECTION]] = TRUE
                    for e in JOINT_ENTRIES[self.map_id][i[DIRECTION]]:
                        self.entry_busy_state[e] = TRUE

                    if i[CARS] < self.min_supported_cars_by_direction[i[DIRECTION]][i[NEW_DIRECTION]]:
                        self.controller.parent_controller.on_create_train(
                            i[TRAIN_ID], i[CARS], ENTRY_TRACK_ID[self.map_id][i[DIRECTION]],
                            APPROACHING_TRAIN_ROUTE[self.map_id][i[DIRECTION]], 'approaching_pass_through',
                            i[DIRECTION], i[DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, PASS_THROUGH_BOARDING_TIME,
                            0.0, 0.0, FALSE
                        )
                    else:
                        self.controller.parent_controller.on_create_train(
                            i[TRAIN_ID], i[CARS], ENTRY_TRACK_ID[self.map_id][i[DIRECTION]],
                            APPROACHING_TRAIN_ROUTE[self.map_id][i[DIRECTION]], 'approaching',
                            i[DIRECTION], i[NEW_DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, i[STOP_TIME],
                            i[EXP], i[MONEY], i[SWITCH_DIRECTION_REQUIRED]
                        )

                    index = BASE_SCHEDULE[self.map_id].index(i)
                    self.view.on_release_train(index)
                    BASE_SCHEDULE[self.map_id].remove(i)
                    break
            else:
                # no more trains can be created because schedule is sorted by arrival time,
                # and arrival time for all following trans will be greater than current time
                break

    @final
    def on_level_up(self):
        super().on_level_up()
        CONFIG_DB_CURSOR.execute(
            '''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
            cars_min, cars_max, switch_direction_required FROM schedule_options 
            WHERE min_level <= ? AND max_level >= ? AND map_id = ?''', (self.level, self.level, self.map_id)
        )
        self.schedule_options = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute(
            '''SELECT schedule_cycle_length, seconds_per_car, exp_per_car, money_per_car FROM map_config 
            WHERE level = ? AND map_id = ?''', (self.level, self.map_id)
        )
        if (schedule_config := CONFIG_DB_CURSOR.fetchone()) is not None:
            self.schedule_cycle_length, self.seconds_per_car, self.exp_per_car, self.money_per_car = schedule_config
        else:
            self.schedule_cycle_length, self.seconds_per_car, self.exp_per_car, self.money_per_car = 0, 0, 0.0, 0.0

    @final
    def on_unlock(self):
        super().on_unlock()
        self.next_cycle_start_time = self.game_time

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        for d in [direction_id for direction_id, (track, environment)
                  in enumerate(MAP_ENTRY_UNLOCK_CONDITIONS[self.map_id])
                  if track == self.unlocked_tracks and environment <= self.unlocked_environment]:
            self.entry_locked_state[d] = FALSE
            if d % 2 == 0:
                self.exit_locked_state[d + 1] = FALSE
            else:
                self.exit_locked_state[d - 1] = FALSE

        self.on_update_min_supported_cars_by_direction()

    @final
    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        for d in [direction_id for direction_id, (track, environment)
                  in enumerate(MAP_ENTRY_UNLOCK_CONDITIONS[self.map_id])
                  if track <= self.unlocked_tracks and environment == self.unlocked_environment]:
            self.entry_locked_state[d] = FALSE
            if d % 2 == 0:
                self.exit_locked_state[d + 1] = FALSE
            else:
                self.exit_locked_state[d - 1] = FALSE

    @final
    def on_leave_entry(self, entry_id):
        self.entry_busy_state[entry_id] = FALSE
        for e in JOINT_ENTRIES[self.map_id][entry_id]:
            self.entry_busy_state[e] = FALSE

    @abstractmethod
    def on_update_min_supported_cars_by_direction(self):
        pass
