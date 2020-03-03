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
        data = f1.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data[::3] + data[1::3] + data[2::3]).hexdigest())

# create database connections and cursors
_user_db_connection: Final = connect(path.join(USER_DB_LOCATION, 'user.db'))
USER_DB_CURSOR: Final = _user_db_connection.cursor()
_config_db_connection: Final = connect('db/config.db')
CONFIG_DB_CURSOR: Final = _config_db_connection.cursor()

# define column titles for all tables
# ---------------------------------
LOG_OPTIONS_LOG_LEVEL: Final = 0
# ---------------------------------
I18N_CURRENT_LOCALE: Final = 0
I18N_CLOCK_24H: Final = 1
# ---------------------------------
NOTIFICATION_SETTINGS_LEVEL_UP_NOTIFICATION_ENABLED: Final = 0
NOTIFICATION_SETTINGS_FEATURE_UNLOCKED_NOTIFICATION_ENABLED: Final = 1
NOTIFICATION_SETTINGS_CONSTRUCTION_COMPLETED_NOTIFICATION_ENABLED: Final = 2
NOTIFICATION_SETTINGS_ENOUGH_MONEY_NOTIFICATION_ENABLED: Final = 3
NOTIFICATION_SETTINGS_BONUS_EXPIRED_NOTIFICATION_ENABLED: Final = 4
NOTIFICATION_SETTINGS_SHOP_STORAGE_NOTIFICATION_ENABLED: Final = 5
# ---------------------------------
GRAPHICS_APP_WIDTH: Final = 0
GRAPHICS_APP_HEIGHT: Final = 1
GRAPHICS_FULLSCREEN: Final = 2
GRAPHICS_DISPLAY_FPS: Final = 3
GRAPHICS_LAST_KNOWN_MAP_ID: Final = 4
GRAPHICS_FADE_ANIMATIONS_ENABLED: Final = 5
# ---------------------------------
MAP_POSITION_SETTINGS_MAP_ID: Final = 0
MAP_POSITION_SETTINGS_LAST_KNOWN_BASE_OFFSET: Final = 1
MAP_POSITION_SETTINGS_LAST_KNOWN_ZOOM: Final = 2
# ---------------------------------
GAME_PROGRESS_LEVEL: Final = 0
GAME_PROGRESS_EXP: Final = 1
GAME_PROGRESS_MONEY: Final = 2
GAME_PROGRESS_MONEY_TARGET: Final = 3
GAME_PROGRESS_ONBOARDING_REQUIRED: Final = 4
GAME_PROGRESS_EXP_MULTIPLIER: Final = 5
GAME_PROGRESS_EXP_BONUS_MULTIPLIER: Final = 6
GAME_PROGRESS_MONEY_BONUS_MULTIPLIER: Final = 7
GAME_PROGRESS_CONSTRUCTION_TIME_BONUS_MULTIPLIER: Final = 8
GAME_PROGRESS_BONUS_CODES_LOCKED: Final = 9
GAME_PROGRESS_BONUS_CODES_ABUSE_COUNTER: Final = 10
# ---------------------------------
MAP_PROGRESS_MAP_ID: Final = 0
MAP_PROGRESS_LOCKED: Final = 1
MAP_PROGRESS_UNLOCKED_TRACKS: Final = 2
MAP_PROGRESS_UNLOCKED_ENVIRONMENT: Final = 3
MAP_PROGRESS_MIN_SUPPORTED_CARS_BY_DIRECTION: Final = 4
MAP_PROGRESS_UNLOCKED_CAR_COLLECTIONS: Final = 5
MAP_PROGRESS_ENTRY_LOCKED_STATE: Final = 6
# ---------------------------------
EPOCH_TIMESTAMP_GAME_TIME: Final = 0
EPOCH_TIMESTAMP_GAME_TIME_FRACTION: Final = 1
EPOCH_TIMESTAMP_DT_MULTIPLIER: Final = 2
# ---------------------------------
CONSTRUCTOR_MAP_ID: Final = 0
CONSTRUCTOR_MONEY_TARGET_ACTIVATED: Final = 1
CONSTRUCTOR_MONEY_TARGET_CELL_POSITION: Final = 2
# ---------------------------------
SCHEDULER_MAP_ID: Final = 0
SCHEDULER_TRAIN_COUNTER: Final = 1
SCHEDULER_NEXT_CYCLE_START_TIME: Final = 2
SCHEDULER_ENTRY_BUSY_STATE: Final = 3
# ---------------------------------
BASE_SCHEDULE_MAP_ID: Final = 0
BASE_SCHEDULE_TRAIN_ID: Final = 1
BASE_SCHEDULE_ARRIVAL: Final = 2
BASE_SCHEDULE_DIRECTION: Final = 3
BASE_SCHEDULE_NEW_DIRECTION: Final = 4
BASE_SCHEDULE_CARS: Final = 5
BASE_SCHEDULE_BOARDING_TIME: Final = 6
BASE_SCHEDULE_EXP: Final = 7
BASE_SCHEDULE_MONEY: Final = 8
BASE_SCHEDULE_SWITCH_DIRECTION_REQUIRED: Final = 9
# ---------------------------------
TRAINS_MAP_ID: Final = 0
TRAINS_TRAIN_ID: Final = 1
TRAINS_CARS: Final = 2
TRAINS_TRAIN_ROUTE_TRACK_NUMBER: Final = 3
TRAINS_TRAIN_ROUTE_TYPE: Final = 4
TRAINS_STATE: Final = 5
TRAINS_DIRECTION: Final = 6
TRAINS_NEW_DIRECTION: Final = 7
TRAINS_CURRENT_DIRECTION: Final = 8
TRAINS_SPEED_STATE: Final = 9
TRAINS_SPEED_STATE_TIME: Final = 10
TRAINS_PRIORITY: Final = 11
TRAINS_BOARDING_TIME: Final = 12
TRAINS_EXP: Final = 13
TRAINS_MONEY: Final = 14
TRAINS_CARS_POSITION: Final = 15
TRAINS_CARS_POSITION_ABS: Final = 16
TRAINS_STOP_POINT: Final = 17
TRAINS_DESTINATION_POINT: Final = 18
TRAINS_CAR_IMAGE_COLLECTION: Final = 19
TRAINS_SWITCH_DIRECTION_REQUIRED: Final = 20
# ---------------------------------
SIGNALS_MAP_ID: Final = 0
SIGNALS_TRACK: Final = 1
SIGNALS_BASE_ROUTE: Final = 2
SIGNALS_STATE: Final = 3
SIGNALS_LOCKED: Final = 4
# ---------------------------------
TRAIN_ROUTES_MAP_ID: Final = 0
TRAIN_ROUTES_TRACK: Final = 1
TRAIN_ROUTES_TRAIN_ROUTE: Final = 2
TRAIN_ROUTES_OPENED: Final = 3
TRAIN_ROUTES_LAST_OPENED_BY: Final = 4
TRAIN_ROUTES_CURRENT_CHECKPOINT: Final = 5
TRAIN_ROUTES_PRIORITY: Final = 6
TRAIN_ROUTES_CARS: Final = 7
TRAIN_ROUTES_TRAIN_ROUTE_SECTION_BUSY_STATE: Final = 8
# ---------------------------------
SWITCHES_MAP_ID: Final = 0
SWITCHES_TRACK_PARAM_1: Final = 1
SWITCHES_TRACK_PARAM_2: Final = 2
SWITCHES_SWITCH_TYPE: Final = 3
SWITCHES_BUSY: Final = 4
SWITCHES_FORCE_BUSY: Final = 5
SWITCHES_LAST_ENTERED_BY: Final = 6
SWITCHES_CURRENT_POSITION: Final = 7
SWITCHES_LOCKED: Final = 8
# ---------------------------------
CROSSOVERS_MAP_ID: Final = 0
CROSSOVERS_TRACK_PARAM_1: Final = 1
CROSSOVERS_TRACK_PARAM_2: Final = 2
CROSSOVERS_CROSSOVER_TYPE: Final = 3
CROSSOVERS_BUSY_1_1: Final = 4
CROSSOVERS_BUSY_1_2: Final = 5
CROSSOVERS_BUSY_2_1: Final = 6
CROSSOVERS_BUSY_2_2: Final = 7
CROSSOVERS_FORCE_BUSY_1_1: Final = 8
CROSSOVERS_FORCE_BUSY_1_2: Final = 9
CROSSOVERS_FORCE_BUSY_2_1: Final = 10
CROSSOVERS_FORCE_BUSY_2_2: Final = 11
CROSSOVERS_LAST_ENTERED_BY_1_1: Final = 12
CROSSOVERS_LAST_ENTERED_BY_1_2: Final = 13
CROSSOVERS_LAST_ENTERED_BY_2_1: Final = 14
CROSSOVERS_LAST_ENTERED_BY_2_2: Final = 15
CROSSOVERS_CURRENT_POSITION_1: Final = 16
CROSSOVERS_CURRENT_POSITION_2: Final = 17
CROSSOVERS_LOCKED: Final = 18
# ---------------------------------
TRACKS_MAP_ID: Final = 0
TRACKS_TRACK_NUMBER: Final = 1
TRACKS_LOCKED: Final = 2
TRACKS_UNDER_CONSTRUCTION: Final = 3
TRACKS_CONSTRUCTION_TIME: Final = 4
TRACKS_BUSY: Final = 5
TRACKS_UNLOCK_CONDITION_FROM_LEVEL: Final = 6
TRACKS_UNLOCK_CONDITION_FROM_PREVIOUS_TRACK: Final = 7
TRACKS_UNLOCK_CONDITION_FROM_ENVIRONMENT: Final = 8
TRACKS_UNLOCK_AVAILABLE: Final = 9
# ---------------------------------
ENVIRONMENT_MAP_ID: Final = 0
ENVIRONMENT_TIER: Final = 1
ENVIRONMENT_LOCKED: Final = 2
ENVIRONMENT_UNDER_CONSTRUCTION: Final = 3
ENVIRONMENT_CONSTRUCTION_TIME: Final = 4
ENVIRONMENT_UNLOCK_CONDITION_FROM_LEVEL: Final = 5
ENVIRONMENT_UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT: Final = 6
ENVIRONMENT_UNLOCK_AVAILABLE: Final = 7
# ---------------------------------
SHOPS_MAP_ID: Final = 0
SHOPS_SHOP_ID: Final = 1
SHOPS_CURRENT_STAGE: Final = 2
SHOPS_SHOP_STORAGE_MONEY: Final = 3
SHOPS_INTERNAL_SHOP_TIME: Final = 4
# ---------------------------------
SHOP_STAGES_MAP_ID: Final = 0
SHOP_STAGES_SHOP_ID: Final = 1
SHOP_STAGES_STAGE_NUMBER: Final = 2
SHOP_STAGES_LOCKED: Final = 3
SHOP_STAGES_UNDER_CONSTRUCTION: Final = 4
SHOP_STAGES_CONSTRUCTION_TIME: Final = 5
SHOP_STAGES_UNLOCK_AVAILABLE: Final = 6
SHOP_STAGES_UNLOCK_CONDITION_FROM_LEVEL: Final = 7
SHOP_STAGES_UNLOCK_CONDITION_FROM_PREVIOUS_STAGE: Final = 8
# ---------------------------------
BONUS_CODES_SHA512_HASH: Final = 0
BONUS_CODES_ACTIVATION_AVAILABLE: Final = 1
BONUS_CODES_ACTIVATIONS_LEFT: Final = 2
BONUS_CODES_IS_ACTIVATED: Final = 3
BONUS_CODES_BONUS_TIME: Final = 4
# ---------------------------------
VERSION_MAJOR: Final = 0
VERSION_MINOR: Final = 1
VERSION_PATCH: Final = 2
# ---------------------------------
SCREEN_RESOLUTION_CONFIG_APP_WIDTH: Final = 0
SCREEN_RESOLUTION_CONFIG_APP_HEIGHT: Final = 1
SCREEN_RESOLUTION_CONFIG_MANUAL_SETUP: Final = 2
# ---------------------------------
PLAYER_PROGRESS_CONFIG_LEVEL: Final = 0
PLAYER_PROGRESS_CONFIG_PLAYER_PROGRESS: Final = 1
# ---------------------------------
MAP_CONFIG_MAP_ID: Final = 0
MAP_CONFIG_LEVEL: Final = 1
MAP_CONFIG_SECONDS_PER_CAR: Final = 2
MAP_CONFIG_EXP_PER_CAR: Final = 3
MAP_CONFIG_MONEY_PER_CAR: Final = 4
MAP_CONFIG_SCHEDULE_CYCLE_LENGTH: Final = 5
# ---------------------------------
MAP_PROGRESS_CONFIG_MAP_ID: Final = 0
MAP_PROGRESS_CONFIG_LEVEL_REQUIRED: Final = 1
MAP_PROGRESS_CONFIG_PRICE: Final = 2
MAP_PROGRESS_CONFIG_UNLOCKED_TRACKS_BY_DEFAULT: Final = 3
# ---------------------------------
SCHEDULE_OPTIONS_MAP_ID: Final = 0
SCHEDULE_OPTIONS_MIN_LEVEL: Final = 1
SCHEDULE_OPTIONS_MAX_LEVEL: Final = 2
SCHEDULE_OPTIONS_ARRIVAL_TIME_MIN: Final = 3
SCHEDULE_OPTIONS_ARRIVAL_TIME_MAX: Final = 4
SCHEDULE_OPTIONS_DIRECTION: Final = 5
SCHEDULE_OPTIONS_NEW_DIRECTION: Final = 6
SCHEDULE_OPTIONS_CARS_MIN: Final = 7
SCHEDULE_OPTIONS_CARS_MAX: Final = 8
SCHEDULE_OPTIONS_SWITCH_DIRECTION_REQUIRED: Final = 9
# ---------------------------------
SIGNAL_CONFIG_MAP_ID: Final = 0
SIGNAL_CONFIG_TRACK: Final = 1
SIGNAL_CONFIG_BASE_ROUTE: Final = 2
SIGNAL_CONFIG_X: Final = 3
SIGNAL_CONFIG_Y: Final = 4
SIGNAL_CONFIG_ROTATION: Final = 5
SIGNAL_CONFIG_TRACK_UNLOCKED_WITH: Final = 6
SIGNAL_CONFIG_ENVIRONMENT_UNLOCKED_WITH: Final = 7
# ---------------------------------
TRAIN_ROUTE_CONFIG_MAP_ID: Final = 0
TRAIN_ROUTE_CONFIG_TRACK: Final = 1
TRAIN_ROUTE_CONFIG_TRAIN_ROUTE: Final = 2
TRAIN_ROUTE_CONFIG_START_POINT_V2: Final = 3
TRAIN_ROUTE_CONFIG_STOP_POINT_V2: Final = 4
TRAIN_ROUTE_CONFIG_DESTINATION_POINT_V2: Final = 5
TRAIN_ROUTE_CONFIG_TRAIL_POINTS_V2_PART_1_START: Final = 6
TRAIN_ROUTE_CONFIG_TRAIL_POINTS_V2_PART_1_END: Final = 7
TRAIN_ROUTE_CONFIG_TRAIL_POINTS_V2_PART_2_HEAD_TAIL: Final = 8
TRAIN_ROUTE_CONFIG_TRAIL_POINTS_V2_PART_2_MID: Final = 9
TRAIN_ROUTE_CONFIG_CHECKPOINTS_V2: Final = 10
# ---------------------------------
TRAIN_ROUTE_SECTIONS_MAP_ID: Final = 0
TRAIN_ROUTE_SECTIONS_TRACK: Final = 1
TRAIN_ROUTE_SECTIONS_TRAIN_ROUTE: Final = 2
TRAIN_ROUTE_SECTIONS_TRACK_PARAM_1: Final = 3
TRAIN_ROUTE_SECTIONS_TRACK_PARAM_2: Final = 4
TRAIN_ROUTE_SECTIONS_SECTION_TYPE: Final = 5
TRAIN_ROUTE_SECTIONS_POSITION_1: Final = 6
TRAIN_ROUTE_SECTIONS_POSITION_2: Final = 7
TRAIN_ROUTE_SECTIONS_SECTION_NUMBER: Final = 8
# ---------------------------------
SWITCHES_CONFIG_MAP_ID: Final = 0
SWITCHES_CONFIG_TRACK_PARAM_1: Final = 1
SWITCHES_CONFIG_TRACK_PARAM_2: Final = 2
SWITCHES_CONFIG_SWITCH_TYPE: Final = 3
SWITCHES_CONFIG_OFFSET_X: Final = 4
SWITCHES_CONFIG_OFFSET_Y: Final = 5
SWITCHES_CONFIG_REGION_X: Final = 6
SWITCHES_CONFIG_REGION_Y: Final = 7
SWITCHES_CONFIG_REGION_W: Final = 8
SWITCHES_CONFIG_REGION_H: Final = 9
SWITCHES_CONFIG_TRACK_UNLOCKED_WITH: Final = 10
SWITCHES_CONFIG_ENVIRONMENT_UNLOCKED_WITH: Final = 11
# ---------------------------------
CROSSOVERS_CONFIG_MAP_ID: Final = 0
CROSSOVERS_CONFIG_TRACK_PARAM_1: Final = 1
CROSSOVERS_CONFIG_TRACK_PARAM_2: Final = 2
CROSSOVERS_CONFIG_CROSSOVER_TYPE: Final = 3
CROSSOVERS_CONFIG_OFFSET_X: Final = 4
CROSSOVERS_CONFIG_OFFSET_Y: Final = 5
CROSSOVERS_CONFIG_REGION_X: Final = 6
CROSSOVERS_CONFIG_REGION_Y: Final = 7
CROSSOVERS_CONFIG_REGION_W: Final = 8
CROSSOVERS_CONFIG_REGION_H: Final = 9
CROSSOVERS_CONFIG_TRACK_UNLOCKED_WITH: Final = 10
CROSSOVERS_CONFIG_ENVIRONMENT_UNLOCKED_WITH: Final = 11
# ---------------------------------
TRACK_CONFIG_MAP_ID: Final = 0
TRACK_CONFIG_TRACK_NUMBER: Final = 1
TRACK_CONFIG_SUPPORTED_CARS_MIN: Final = 2
TRACK_CONFIG_SUPPORTED_CARS_MAX: Final = 3
TRACK_CONFIG_PRICE: Final = 4
TRACK_CONFIG_MAX_CONSTRUCTION_TIME: Final = 5
TRACK_CONFIG_LEVEL: Final = 6
TRACK_CONFIG_ENVIRONMENT_TIER: Final = 7
# ---------------------------------
ENVIRONMENT_CONFIG_MAP_ID: Final = 0
ENVIRONMENT_CONFIG_TIER: Final = 1
ENVIRONMENT_CONFIG_PRICE: Final = 2
ENVIRONMENT_CONFIG_MAX_CONSTRUCTION_TIME: Final = 3
ENVIRONMENT_CONFIG_LEVEL: Final = 4
# ---------------------------------
SHOPS_CONFIG_MAP_ID: Final = 0
SHOPS_CONFIG_SHOP_ID: Final = 1
SHOPS_CONFIG_TRACK_REQUIRED: Final = 2
SHOPS_CONFIG_LEVEL_REQUIRED: Final = 3
SHOPS_CONFIG_BUTTON_X: Final = 4
SHOPS_CONFIG_BUTTON_Y: Final = 5
# ---------------------------------
SHOP_PROGRESS_CONFIG_MAP_ID: Final = 0
SHOP_PROGRESS_CONFIG_STAGE_NUMBER: Final = 1
SHOP_PROGRESS_CONFIG_LEVEL_REQUIRED: Final = 2
SHOP_PROGRESS_CONFIG_PRICE: Final = 3
SHOP_PROGRESS_CONFIG_MAX_CONSTRUCTION_TIME: Final = 4
SHOP_PROGRESS_CONFIG_HOURLY_PROFIT: Final = 5
SHOP_PROGRESS_CONFIG_STORAGE_CAPACITY: Final = 6
SHOP_PROGRESS_CONFIG_EXP_BONUS: Final = 7
# ---------------------------------
BONUS_CODES_CONFIG_SHA512_HASH: Final = 0
BONUS_CODES_CONFIG_CODE_TYPE: Final = 1
BONUS_CODES_CONFIG_BONUS_VALUE: Final = 2
BONUS_CODES_CONFIG_LEVEL_REQUIRED: Final = 3
BONUS_CODES_CONFIG_MAX_BONUS_TIME: Final = 4
# ---------------------------------


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    _user_db_connection.commit()
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
