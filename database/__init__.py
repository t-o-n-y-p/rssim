from sqlite3 import connect
from os import path, makedirs
from shutil import copyfile
from hashlib import sha512
from typing import Final, final

from keyring import set_password, delete_password, set_keyring
from keyring.errors import PasswordDeleteError
from keyring.backends import Windows
from pyglet.resource import get_settings_path


set_keyring(Windows.WinVaultKeyring())
# determine if user launches app for the first time, if yes - create game DB
USER_DB_LOCATION: Final = get_settings_path("Railway Station Simulator")
_user_db_full_path = path.join(USER_DB_LOCATION, 'user.db')
if not path.exists(USER_DB_LOCATION):
    makedirs(USER_DB_LOCATION)

if not path.exists(_user_db_full_path):
    copyfile('db/default.db', _user_db_full_path)
    try:
        delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open(_user_db_full_path, 'rb') as f1:
        _data = f1.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(_data[::3] + _data[1::3] + _data[2::3]).hexdigest())

# create database connections and cursors
USER_DB_CONNECTION: Final = connect(path.join(USER_DB_LOCATION, 'user.db'))
USER_DB_CURSOR: Final = USER_DB_CONNECTION.cursor()
_config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR: Final = _config_db_connection.cursor()

# time
SECONDS_IN_ONE_MINUTE: Final = 60
MINUTES_IN_ONE_HOUR: Final = 60
SECONDS_IN_ONE_HOUR: Final = SECONDS_IN_ONE_MINUTE * MINUTES_IN_ONE_HOUR
HOURS_IN_ONE_DAY: Final = 24
SECONDS_IN_ONE_DAY: Final = SECONDS_IN_ONE_MINUTE * MINUTES_IN_ONE_HOUR * HOURS_IN_ONE_DAY

TRUE: Final = 1
FALSE: Final = 0

TRACKS: Final = 0
ENVIRONMENT: Final = 1

PASSENGER_MAP: Final = 0
FREIGHT_MAP: Final = 1

CONSTRUCTOR_VIEW_TRACK_CELLS: Final = 4                # number of cells for tracks on constructor screen
CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS: Final = 4          # number of cells for environment tiers on constructor screen
# bonus code matrix properties
CODE_TYPE: Final = 0
BONUS_VALUE: Final = 1
REQUIRED_LEVEL: Final = 2
MAXIMUM_BONUS_TIME: Final = 3
ACTIVATION_AVAILABLE: Final = 4
ACTIVATIONS_LEFT: Final = 5
IS_ACTIVATED: Final = 6
BONUS_TIME: Final = 7

BONUS_CODE_MATRIX = {}
CONFIG_DB_CURSOR.execute('''SELECT * FROM bonus_codes_config''')
for _line in CONFIG_DB_CURSOR.fetchall():
    BONUS_CODE_MATRIX[_line[0]] = [*_line[1:]]
    USER_DB_CURSOR.execute('''SELECT activation_available, activations_left, is_activated, bonus_time
                              FROM bonus_codes WHERE sha512_hash = ?''', (_line[0],))
    BONUS_CODE_MATRIX[_line[0]].extend(USER_DB_CURSOR.fetchone())

# base_schedule matrix properties
TRAIN_ID: Final = 0                            # property #0 indicates train identification number
ARRIVAL_TIME: Final = 1                        # property #1 indicates arrival time
DIRECTION: Final = 2                           # property #2 indicates direction
NEW_DIRECTION: Final = 3                       # property #3 indicates new direction
CARS: Final = 4                                # property #4 indicates number of cars
STOP_TIME: Final = 5                           # property #5 indicates how much stop time left
EXP: Final = 6                                 # property #6 indicates how much exp the train gives
MONEY: Final = 7                               # property #7 indicates how much money the train gives
SWITCH_DIRECTION_REQUIRED: Final = 8

# schedule options matrix properties
ARRIVAL_TIME_MIN: Final = 0             # property #0 indicates min arrival time offset from the beginning of the cycle
ARRIVAL_TIME_MAX: Final = 1             # property #1 indicates max arrival time offset from the beginning of the cycle
# property #2 indicates direction
# property #3 indicates new direction
CARS_MIN: Final = 4                     # property #4 indicates min number of cars
CARS_MAX: Final = 5                     # property #5 indicates max number of cars
SWITCH_DIRECTION_FLAG = 6

BASE_SCHEDULE = [(), ()]
for _m in (PASSENGER_MAP, FREIGHT_MAP):
    USER_DB_CURSOR.execute('''SELECT train_id, arrival, direction, new_direction, 
                              cars, boarding_time, exp, money, switch_direction_required 
                              FROM base_schedule WHERE map_id = ?''', (_m,))
    BASE_SCHEDULE[_m] = USER_DB_CURSOR.fetchall()

CONSTRUCTION_STATE_MATRIX = [[{}, {}], [{}, {}]]
for _m in (PASSENGER_MAP, FREIGHT_MAP):
    USER_DB_CURSOR.execute('''SELECT track_number, locked, under_construction, construction_time, 
                              unlock_condition_from_level, unlock_condition_from_previous_track, 
                              unlock_condition_from_environment, unlock_available FROM tracks 
                              WHERE locked = 1 AND map_id = ?''', (_m,))
    _track_info_fetched = USER_DB_CURSOR.fetchall()
    for _info in _track_info_fetched:
        CONSTRUCTION_STATE_MATRIX[_m][TRACKS][_info[0]] = list(_info[1:])
        CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level, environment_tier FROM track_config 
                                    WHERE track_number = ? AND map_id = ?''', (_info[0], _m))
        CONSTRUCTION_STATE_MATRIX[_m][TRACKS][_info[0]].extend(CONFIG_DB_CURSOR.fetchone())

    USER_DB_CURSOR.execute('''SELECT tier, locked, under_construction, construction_time, 
                              unlock_condition_from_level, unlock_condition_from_previous_environment,
                              unlock_available FROM environment WHERE locked = 1 AND map_id = ?''', (_m,))
    _environment_info_fetched = USER_DB_CURSOR.fetchall()
    for _info in _environment_info_fetched:
        CONSTRUCTION_STATE_MATRIX[_m][ENVIRONMENT][_info[0]] = [*_info[1:6], 1, _info[6]]
        CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level FROM environment_config 
                                    WHERE tier = ? AND map_id = ?''', (_info[0], _m))
        CONSTRUCTION_STATE_MATRIX[_m][ENVIRONMENT][_info[0]].extend(CONFIG_DB_CURSOR.fetchone())

# track, environment and shop stage state matrix properties
LOCKED: Final = 0                                      # property #0 indicates if track/env. is locked
UNDER_CONSTRUCTION: Final = 1                          # property #1 indicates if track/env. is under construction
CONSTRUCTION_TIME: Final = 2                           # property #2 indicates construction time left
UNLOCK_CONDITION_FROM_LEVEL: Final = 3                 # property #3 indicates if unlock condition from level is met
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK: Final = 4        # property #4 indicates if unlock previous track condition is met
UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT: Final = 4  # property #4 indicates if unlock previous env. condition is met
UNLOCK_CONDITION_FROM_PREVIOUS_STAGE: Final = 4        # property #4 indicates if unlock previous stage condition is met
UNLOCK_CONDITION_FROM_ENVIRONMENT: Final = 5           # indicates if unlock environment condition is met (tracks only)
UNLOCK_AVAILABLE: Final = 6                            # property #6 indicates if all unlock conditions are met
PRICE: Final = 7                                       # property #7 indicates track/env. price
MAX_CONSTRUCTION_TIME: Final = 8
LEVEL_REQUIRED: Final = 9                              # property #9 indicates required level for this track/env.
ENVIRONMENT_REQUIRED: Final = 10                       # property #10 indicates required environment tier (tracks only)
HOURLY_PROFIT: Final = 11
STORAGE_CAPACITY: Final = 12
EXP_BONUS: Final = 13

MAP_SWITCHER_STATE_MATRIX = [[], []]
for _m in (PASSENGER_MAP, FREIGHT_MAP):
    USER_DB_CURSOR.execute('''SELECT locked FROM map_progress WHERE map_id = ?''', (_m,))
    MAP_SWITCHER_STATE_MATRIX[_m].append(USER_DB_CURSOR.fetchone()[0])
    CONFIG_DB_CURSOR.execute('''SELECT level_required, price FROM map_progress_config WHERE map_id = ?''', (_m,))
    MAP_SWITCHER_STATE_MATRIX[_m].extend(CONFIG_DB_CURSOR.fetchone())

MAP_LOCKED: Final = 0
MAP_LEVEL_REQUIRED: Final = 1
MAP_PRICE: Final = 2

NARRATOR_QUEUE = [[], []]
for _m in (PASSENGER_MAP, FREIGHT_MAP):
    USER_DB_CURSOR.execute('''SELECT game_time, locked, announcement_type, train_id, track_number 
                              FROM narrator WHERE map_id = ?''', (_m,))
    NARRATOR_QUEUE[_m] = [list(a) for a in USER_DB_CURSOR.fetchall()]

ANNOUNCEMENT_TIME: Final = 0
ANNOUNCEMENT_LOCKED: Final = 1
ANNOUNCEMENT_TYPE: Final = 2
ANNOUNCEMENT_TRAIN_ID: Final = 3
ANNOUNCEMENT_TRACK_NUMBER: Final = 4

ARRIVAL_ANNOUNCEMENT: Final = 'arrival'
ARRIVAL_FINISHED_ANNOUNCEMENT: Final = 'arrival_finished'
DEPARTURE_ANNOUNCEMENT: Final = 'departure'
PASS_THROUGH_ANNOUNCEMENT: Final = 'pass_through'
FIVE_MINUTES_LEFT_ANNOUNCEMENT: Final = 'five_minutes_left'


def get_announcement_types_enabled(dt_multiplier):
    if round(dt_multiplier, 1) > 8.0:
        return ARRIVAL_ANNOUNCEMENT, PASS_THROUGH_ANNOUNCEMENT
    elif round(dt_multiplier, 1) > 4.0:
        return get_announcement_types_enabled(12) + (DEPARTURE_ANNOUNCEMENT, )

    return get_announcement_types_enabled(6) + (ARRIVAL_FINISHED_ANNOUNCEMENT, FIVE_MINUTES_LEFT_ANNOUNCEMENT)


def get_announcement_types_diff(dt_multiplier_1, dt_multiplier_2):
    return [announcement for announcement in get_announcement_types_enabled(min(dt_multiplier_1, dt_multiplier_2))
            if announcement not in get_announcement_types_enabled(max(dt_multiplier_1, dt_multiplier_2))]


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    USER_DB_CONNECTION.commit()
    with open(_user_db_full_path, 'rb') as f:
        data1 = f.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data1[::3] + data1[1::3] + data1[2::3]).hexdigest())


@final
class TrailPointsV2:
    def __init__(self, map_id, track, train_route):
        CONFIG_DB_CURSOR.execute('''SELECT trail_points_v2_part_1_start, trail_points_v2_part_1_end
                                    FROM train_route_config WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (track, train_route, map_id))
        self.part_1_start, part_1_end = (tuple(float(p) for p in s.split(',')) for s in CONFIG_DB_CURSOR.fetchone())
        CONFIG_DB_CURSOR.execute('''SELECT trail_points_v2_part_2_head_tail, trail_points_v2_part_2_mid
                                    FROM train_route_config WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (track, train_route, map_id))
        self.part_2_head_tail, self.part_2_mid = CONFIG_DB_CURSOR.fetchone()
        if self.part_2_head_tail is not None:
            self.part_2_head_tail = tuple(
                tuple(float(p) for p in s.split(',')) for s in self.part_2_head_tail.split('|')
            )

        if self.part_2_mid is None:
            self.part_2_mid = self.part_2_head_tail
        else:
            self.part_2_mid = tuple(
                tuple(float(p) for p in s.split(',')) for s in self.part_2_mid.split('|')
            )

        self.part_1_length = round(part_1_end[0] - self.part_1_start[0])
        self.multiplier = self.part_1_length // abs(self.part_1_length)
        self.part_1_length = abs(self.part_1_length)
        self.part_2_length = None
        self.part_3_start = None
        if self.part_2_head_tail is not None:
            self.part_2_length = self.part_1_length + len(self.part_2_head_tail) - 1
            self.part_3_start = self.part_2_head_tail[-1]

    def get_head_tail_car_position(self, index):
        if index < self.part_1_length:
            return self.part_1_start[0] + self.multiplier * index, *self.part_1_start[1:]
        elif index < self.part_2_length:
            index -= self.part_1_length
            return tuple(self.part_2_head_tail[int(index)][i]
                         + (self.part_2_head_tail[int(index) + 1][i] - self.part_2_head_tail[int(index)][i])
                         * (index % 1) for i in range(3))
        else:
            index -= self.part_2_length
            return self.part_3_start[0] + self.multiplier * index, *self.part_3_start[1:]

    def get_mid_car_position(self, index):
        if index < self.part_1_length:
            return self.part_1_start[0] + self.multiplier * index, *self.part_1_start[1:]
        elif index < self.part_2_length:
            index -= self.part_1_length
            return tuple(self.part_2_mid[int(index)][i]
                         + (self.part_2_mid[int(index) + 1][i] - self.part_2_mid[int(index)][i])
                         * (index % 1) for i in range(3))
        else:
            index -= self.part_2_length
            return self.part_3_start[0] + self.multiplier * index, *self.part_3_start[1:]

    def get_conversion_index(self, car_position):
        if self.part_2_length is not None:
            car_position -= self.part_2_length
            return self.part_3_start[0] + self.multiplier * car_position, self.part_3_start[1]
        else:
            return self.part_1_start[0] + self.multiplier * car_position, self.part_1_start[1]

    def get_reconversion_index(self, car_position_abs):
        return float(abs(car_position_abs[0] - self.part_1_start[0]))
