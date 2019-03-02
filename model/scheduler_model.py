from random import choice
from operator import itemgetter
from logging import getLogger

from model import *


class SchedulerModel(Model):
    """
    Implements Scheduler model.
    Scheduler object is responsible for properties, UI and events related to the train schedule.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            level                               current player level
            unlocked_tracks                     indicates how much tracks are available at the moment
            supported_cars_min                  indicates minimum number of cars all track can handle
                                                (except 1st and 2nd)
            schedule_options                    matrix with info about schedule cycles at current level
            base_schedule                       generated train queue sorted by arrival time
            train_counter                       ID for next train
            entry_busy_state                    indicates if train entries (from 0 to 3 based on direction) are busy
            next_cycle_start_time               in-game timestamp for next schedule cycle beginning
            schedule_cycle_length               length of schedule cycle at current level in frames
            frame_per_car                       property to calculate boarding time for train
                                                based on level and number of cars
            exp_per_car                         property to calculate exp for train
                                                based on level and number of cars
            money_per_car                       property to calculate money gained for train
                                                based on level and number of cars

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.scheduler.model'))
        self.user_db_cursor.execute('SELECT level, unlocked_tracks, supported_cars_min FROM game_progress')
        self.level, self.unlocked_tracks, self.supported_cars_min = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options 
                                      WHERE min_level <= ? AND max_level >= ?''', (self.level, self.level))
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
        """
        Activates the model. Does not activate the view because schedule screen is not opened by default.
        """
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_activate_view(self):
        """
        Activates the Scheduler view.
        """
        self.view.on_activate()

    def on_update_time(self, game_time):
        """
        Creates one more schedule cycle is necessary.
        Notifies Map controller to create train if arrival time is less or equal to current time
        and corresponding entry is not busy.

        :param game_time:               current in-game time
        """
        # new schedule cycle is created if current schedule end is less than schedule cycle length ahead
        if game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            # trains are added one by one if both direction and new direction are unlocked by user,
            # otherwise train is skipped
            for i in self.schedule_options:
                if (i[DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)
                        and i[NEW_DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)) \
                        or ((i[DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE)
                            and self.unlocked_tracks >= LEFT_SIDE_ENTRY_FIRST_TRACK)\
                        or ((i[DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE)
                            and self.unlocked_tracks >= RIGHT_SIDE_ENTRY_FIRST_TRACK):
                    cars = choice([i[CARS_MIN], i[CARS_MAX]])
                    train_options = (self.train_counter, self.next_cycle_start_time
                                     + choice(list(range(i[ARRIVAL_TIME_MIN], i[ARRIVAL_TIME_MAX]))),
                                     i[DIRECTION], i[NEW_DIRECTION], cars, self.frame_per_car * cars,
                                     self.exp_per_car * cars, self.money_per_car * cars)
                    self.base_schedule.append(train_options)
                    self.train_counter = (self.train_counter + 1) % TRAIN_ID_LIMIT

            self.next_cycle_start_time += self.schedule_cycle_length
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(ARRIVAL_TIME))

        # notify the view about both base_schedule and/or game_time update
        self.view.on_update_live_schedule(self.base_schedule, game_time)
        # notify Map controller about new train available if arrival time is less or equal than current time
        # and corresponding entry is not busy; only one train at a time is created
        for i in self.base_schedule:
            if game_time >= i[ARRIVAL_TIME]:
                if not self.entry_busy_state[i[DIRECTION]]:
                    self.entry_busy_state[i[DIRECTION]] = True
                    if i[CARS] < self.supported_cars_min:
                        state = 'approaching_pass_through'
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK[i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[i[DIRECTION]], state, i[DIRECTION],
                                             i[DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, PASS_THROUGH_BOARDING_TIME,
                                             0.0, 0.0)
                    else:
                        state = 'approaching'
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK[i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[i[DIRECTION]], state, i[DIRECTION],
                                             i[NEW_DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, i[STOP_TIME],
                                             i[EXP], i[MONEY])

                    index = self.base_schedule.index(i)
                    self.base_schedule.remove(i)
                    self.view.on_release_train(index)
                    break
            else:
                # no more trains can be created because schedule is sorted by arrival time,
                # and arrival time for all following trans will be greater than current time
                break

    def on_save_state(self):
        """
        Saves schedule matrix to user progress database.
        """
        entry_busy_state_string = '{},{},{},{}'.format(int(self.entry_busy_state[0]), int(self.entry_busy_state[1]),
                                                       int(self.entry_busy_state[2]), int(self.entry_busy_state[3]))
        self.user_db_cursor.execute('''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, 
                                       entry_busy_state = ?''',
                                    (self.train_counter, self.next_cycle_start_time, entry_busy_state_string))
        self.user_db_cursor.execute('DELETE FROM base_schedule')
        self.user_db_cursor.executemany('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.base_schedule)
        self.user_db_cursor.execute('UPDATE game_progress SET supported_cars_min = ?', (self.supported_cars_min, ))

    def on_level_up(self, level):
        """
        Reads new level-dependent data when user hits new level.

        :param level:                   new level value
        """
        self.level = level
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options 
                                      WHERE min_level <= ? AND max_level >= ?''', (self.level, self.level))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks and supported cars.

        :param track:                   track number
        """
        self.unlocked_tracks = track
        self.config_db_cursor.execute('SELECT supported_cars_min FROM track_config WHERE track_number = ?',
                                      (track, ))
        self.supported_cars_min = self.config_db_cursor.fetchone()[0]

    def on_leave_entry(self, entry_id):
        """
        Updates entry state.

        :param entry_id:                        entry identification number from 0 to 3
        """
        self.entry_busy_state[entry_id] = False
