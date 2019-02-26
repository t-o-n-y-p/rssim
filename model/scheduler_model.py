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
        self.logger.info('START INIT')
        self.user_db_cursor.execute('SELECT level, unlocked_tracks, supported_cars_min FROM game_progress')
        self.level, self.unlocked_tracks, self.supported_cars_min = self.user_db_cursor.fetchone()
        self.logger.debug(f'level: {self.level}')
        self.logger.debug(f'unlocked_tracks: {self.unlocked_tracks}')
        self.logger.debug(f'supported_cars_min: {self.supported_cars_min}')
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options WHERE level = ?''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.logger.debug(f'schedule_options: {self.schedule_options}')
        self.user_db_cursor.execute('SELECT * FROM base_schedule')
        self.base_schedule = self.user_db_cursor.fetchall()
        self.logger.debug(f'base_schedule: {self.base_schedule}')
        self.user_db_cursor.execute('SELECT train_counter, next_cycle_start_time FROM scheduler')
        self.train_counter, self.next_cycle_start_time = self.user_db_cursor.fetchone()
        self.logger.debug(f'train_counter: {self.train_counter}')
        self.logger.debug(f'next_cycle_start_time: {self.next_cycle_start_time}')
        self.user_db_cursor.execute('SELECT entry_busy_state FROM scheduler')
        entry_busy_state_parsed = self.user_db_cursor.fetchone()[0].split(',')
        for i in range(len(entry_busy_state_parsed)):
            entry_busy_state_parsed[i] = bool(int(entry_busy_state_parsed[i]))

        self.entry_busy_state = entry_busy_state_parsed
        self.logger.debug(f'entry_busy_state: {self.entry_busy_state}')
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()
        self.logger.debug(f'schedule_cycle_length: {self.schedule_cycle_length}')
        self.logger.debug(f'frame_per_car: {self.frame_per_car}')
        self.logger.debug(f'exp_per_car: {self.exp_per_car}')
        self.logger.debug(f'money_per_car: {self.money_per_car}')
        self.logger.info('END INIT')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model. Does not activate the view because schedule screen is not opened by default.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_ACTIVATE')

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_activate_view(self):
        """
        Activates the Scheduler view.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_activate()
        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_update_time(self, game_time):
        """
        Creates one more schedule cycle is necessary.
        Notifies Map controller to create train if arrival time is less or equal to current time
        and corresponding entry is not busy.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
        self.logger.debug(f'game_time: {game_time}')
        self.logger.debug(f'schedule_cycle_length: {self.schedule_cycle_length}')
        self.logger.debug(f'next_cycle_start_time: {self.next_cycle_start_time}')
        # new schedule cycle is created if current schedule end is less than schedule cycle length ahead
        if game_time + self.schedule_cycle_length >= self.next_cycle_start_time:
            self.logger.debug('creating new schedule cycle')
            # trains are added one by one if both direction and new direction are unlocked by user,
            # otherwise train is skipped
            for i in self.schedule_options:
                self.logger.debug(f'direction: {i[DIRECTION]}')
                self.logger.debug(f'new_direction: {i[NEW_DIRECTION]}')
                self.logger.debug(f'unlocked_tracks: {self.unlocked_tracks}')
                if (i[DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)
                        and i[NEW_DIRECTION] in (DIRECTION_FROM_LEFT_TO_RIGHT, DIRECTION_FROM_RIGHT_TO_LEFT)) \
                        or ((i[DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE)
                            and self.unlocked_tracks >= LEFT_SIDE_ENTRY_FIRST_TRACK)\
                        or ((i[DIRECTION] == DIRECTION_FROM_RIGHT_TO_LEFT_SIDE
                             or i[NEW_DIRECTION] == DIRECTION_FROM_LEFT_TO_RIGHT_SIDE)
                            and self.unlocked_tracks >= RIGHT_SIDE_ENTRY_FIRST_TRACK):
                    self.logger.debug('all conditions are met, creating this train')
                    cars = choice([i[CARS_MIN], i[CARS_MAX]])
                    self.logger.debug(f'cars: {cars}')
                    train_options = (self.train_counter, self.next_cycle_start_time
                                     + choice(list(range(i[ARRIVAL_TIME_MIN], i[ARRIVAL_TIME_MAX]))),
                                     i[DIRECTION], i[NEW_DIRECTION], cars, self.frame_per_car * cars,
                                     self.exp_per_car * cars, self.money_per_car * cars)
                    self.logger.debug(f'train_options: {train_options}')
                    self.base_schedule.append(train_options)
                    self.logger.debug(f'base_schedule: {self.base_schedule}')
                    self.train_counter = (self.train_counter + 1) % TRAIN_ID_LIMIT
                    self.logger.debug(f'train_counter: {self.train_counter}')
                else:
                    self.logger.debug('cannot create train: required track not unlocked')

            self.logger.debug(f'next_cycle_start_time: {self.next_cycle_start_time}')
            self.logger.debug(f'schedule_cycle_length: {self.schedule_cycle_length}')
            self.next_cycle_start_time += self.schedule_cycle_length
            self.logger.debug(f'next_cycle_start_time: {self.next_cycle_start_time}')
            self.base_schedule = sorted(self.base_schedule, key=itemgetter(ARRIVAL_TIME))
            self.logger.debug(f'base_schedule: {self.base_schedule}')
        else:
            self.logger.debug('no need to create new schedule cycle')

        # notify the view about both base_schedule and/or game_time update
        self.view.on_update_live_schedule(self.base_schedule, game_time)
        # notify Map controller about new train available if arrival time is less or equal than current time
        # and corresponding entry is not busy; only one train at a time is created
        self.logger.debug(f'base_schedule: {self.base_schedule}')
        for i in self.base_schedule:
            self.logger.debug(f'game_time: {game_time}')
            self.logger.debug(f'arrival_time: {i[ARRIVAL_TIME]}')
            if game_time >= i[ARRIVAL_TIME]:
                self.logger.debug(f'direction {i[DIRECTION]} entry_busy_state: {self.entry_busy_state[i[DIRECTION]]}')
                if not self.entry_busy_state[i[DIRECTION]]:
                    self.entry_busy_state[i[DIRECTION]] = True
                    self.logger.debug(
                        f'direction {i[DIRECTION]} entry_busy_state: {self.entry_busy_state[i[DIRECTION]]}'
                    )
                    self.logger.debug(f'cars: {i[CARS]}')
                    self.logger.debug(f'supported_cars_min: {self.supported_cars_min}')
                    if i[CARS] < self.supported_cars_min:
                        state = 'approaching_pass_through'
                        self.logger.debug(f'state: {state}')
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK[i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[i[DIRECTION]], state, i[DIRECTION],
                                             i[DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, PASS_THROUGH_BOARDING_TIME,
                                             0.0, 0.0)
                    else:
                        state = 'approaching'
                        self.logger.debug(f'state: {state}')
                        self.controller.parent_controller\
                            .on_create_train(i[TRAIN_ID], i[CARS], ENTRY_TRACK[i[DIRECTION]],
                                             APPROACHING_TRAIN_ROUTE[i[DIRECTION]], state, i[DIRECTION],
                                             i[NEW_DIRECTION], i[DIRECTION], DEFAULT_PRIORITY, i[STOP_TIME],
                                             i[EXP], i[MONEY])

                    index = self.base_schedule.index(i)
                    self.logger.debug(f'index: {index}')
                    self.logger.debug(f'base_schedule: {self.base_schedule}')
                    self.base_schedule.remove(i)
                    self.logger.debug(f'base_schedule: {self.base_schedule}')
                    self.view.on_release_train(index)
                    break
            else:
                # no more trains can be created because schedule is sorted by arrival time,
                # and arrival time for all following trans will be greater than current time
                break

        self.logger.info('END ON_UPDATE_TIME')

    def on_save_state(self):
        """
        Saves schedule matrix to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        entry_busy_state_string = '{},{},{},{}'.format(int(self.entry_busy_state[0]), int(self.entry_busy_state[1]),
                                                       int(self.entry_busy_state[2]), int(self.entry_busy_state[3]))
        self.logger.debug(f'entry_busy_state_string: {entry_busy_state_string}')
        self.logger.debug(f'train_counter: {self.train_counter}')
        self.logger.debug(f'next_cycle_start_time: {self.next_cycle_start_time}')
        self.user_db_cursor.execute('''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, 
                                       entry_busy_state = ?''',
                                    (self.train_counter, self.next_cycle_start_time, entry_busy_state_string))
        self.logger.debug('entry_busy_state, train_counter, next_cycle_start_time saved successfully')
        self.user_db_cursor.execute('DELETE FROM base_schedule')
        self.logger.debug('old schedule removed')
        self.logger.debug(f'base_schedule: {self.base_schedule}')
        self.user_db_cursor.executemany('INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.base_schedule)
        self.logger.debug('base_schedule saved successfully')
        self.logger.debug(f'supported_cars_min: {self.supported_cars_min}')
        self.user_db_cursor.execute('UPDATE game_progress SET supported_cars_min = ?', (self.supported_cars_min, ))
        self.logger.debug('supported_cars_min saved successfully')
        self.logger.info('END ON_SAVE_STATE')

    def on_level_up(self, level):
        """
        Reads new level-dependent data when user hits new level.

        :param level:                   new level value
        """
        self.logger.info('START ON_LEVEL_UP')
        self.level = level
        self.logger.debug(f'level: {self.level}')
        self.config_db_cursor.execute('''SELECT arrival_time_min, arrival_time_max, direction, new_direction, 
                                      cars_min, cars_max FROM schedule_options WHERE level = ?''', (self.level, ))
        self.schedule_options = self.config_db_cursor.fetchall()
        self.logger.debug(f'schedule_options: {self.schedule_options}')
        self.config_db_cursor.execute('''SELECT schedule_cycle_length, frame_per_car, exp_per_car, money_per_car 
                                      FROM player_progress_config WHERE level = ?''',
                                      (self.level, ))
        self.schedule_cycle_length, self.frame_per_car, self.exp_per_car, self.money_per_car \
            = self.config_db_cursor.fetchone()
        self.logger.debug(f'schedule_cycle_length: {self.schedule_cycle_length}')
        self.logger.debug(f'frame_per_car: {self.frame_per_car}')
        self.logger.debug(f'exp_per_car: {self.exp_per_car}')
        self.logger.debug(f'money_per_car: {self.money_per_car}')
        self.logger.info('END ON_LEVEL_UP')

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks and supported cars.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK')
        self.unlocked_tracks = track
        self.logger.debug(f'unlocked_tracks: {self.unlocked_tracks}')
        self.config_db_cursor.execute('SELECT supported_cars_min FROM track_config WHERE track_number = ?',
                                      (track, ))
        self.supported_cars_min = self.config_db_cursor.fetchone()[0]
        self.logger.debug(f'supported_cars_min: {self.supported_cars_min}')
        self.logger.info('END ON_UNLOCK_TRACK')

    def on_leave_entry(self, entry_id):
        """
        Updates entry state.

        :param entry_id:                        entry identification number from 0 to 3
        """
        self.logger.info('START ON_LEAVE_ENTRY')
        self.entry_busy_state[entry_id] = False
        self.logger.debug(f'direction {entry_id} entry state: {self.entry_busy_state[entry_id]}')
        self.logger.info('END ON_LEAVE_ENTRY')
