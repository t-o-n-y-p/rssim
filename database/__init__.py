from sqlite3 import connect
from os import path, makedirs
from shutil import copyfile
from hashlib import sha512
from typing import Final

from keyring import set_password, delete_password, set_keyring
from keyring.errors import PasswordDeleteError
from keyring.backends import Windows
from pyglet.resource import get_settings_path


set_keyring(Windows.WinVaultKeyring())
# determine if user launches app for the first time, if yes - create game DB
USER_DB_LOCATION: Final = get_settings_path(sha512('rssim'.encode('utf-8')).hexdigest())
__user_db_full_path = path.join(USER_DB_LOCATION, 'user.db')
if not path.exists(USER_DB_LOCATION):
    makedirs(USER_DB_LOCATION)

if not path.exists(__user_db_full_path):
    copyfile('db/default.db', __user_db_full_path)
    try:
        delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open(__user_db_full_path, 'rb') as f1:
        data = f1.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data[::3] + data[1::3] + data[2::3]).hexdigest())

# create database connections and cursors
USER_DB_CONNECTION: Final = connect(path.join(USER_DB_LOCATION, 'user.db'))
USER_DB_CURSOR: Final = USER_DB_CONNECTION.cursor()
__config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR: Final = __config_db_connection.cursor()

TRACKS = 0
ENVIRONMENT = 1

PASSENGER_MAP = 0
FREIGHT_MAP = 1
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
for line in CONFIG_DB_CURSOR.fetchall():
    BONUS_CODE_MATRIX[line[0]] = [*line[1:]]
    USER_DB_CURSOR.execute('''SELECT activation_available, activations_left, is_activated, bonus_time
                              FROM bonus_codes WHERE sha512_hash = ?''', (line[0],))
    BONUS_CODE_MATRIX[line[0]].extend(USER_DB_CURSOR.fetchone())
    BONUS_CODE_MATRIX[line[0]][ACTIVATION_AVAILABLE] \
        = bool(BONUS_CODE_MATRIX[line[0]][ACTIVATION_AVAILABLE])
    BONUS_CODE_MATRIX[line[0]][IS_ACTIVATED] \
        = bool(BONUS_CODE_MATRIX[line[0]][IS_ACTIVATED])

BASE_SCHEDULE = [(), ()]
USER_DB_CURSOR.execute('''SELECT train_id, arrival, direction, new_direction, 
                          cars, boarding_time, exp, money, switch_direction_required 
                          FROM base_schedule WHERE map_id = 0''')
BASE_SCHEDULE[PASSENGER_MAP] = USER_DB_CURSOR.fetchall()

CONSTRUCTION_STATE_MATRIX = [[{}, {}], [{}, {}]]
USER_DB_CURSOR.execute('''SELECT track_number, locked, under_construction, construction_time, 
                          unlock_condition_from_level, unlock_condition_from_previous_track, 
                          unlock_condition_from_environment, unlock_available FROM tracks 
                          WHERE locked = 1 AND map_id = 0''')
track_info_fetched = USER_DB_CURSOR.fetchall()
for info in track_info_fetched:
    CONSTRUCTION_STATE_MATRIX[PASSENGER_MAP][TRACKS][info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]),
                                                                 bool(info[5]), bool(info[6]), bool(info[7])]
    CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level, environment_tier FROM track_config 
                                WHERE track_number = ? AND map_id = 0''', (info[0], ))
    CONSTRUCTION_STATE_MATRIX[PASSENGER_MAP][TRACKS][info[0]].extend(CONFIG_DB_CURSOR.fetchone())

USER_DB_CURSOR.execute('''SELECT tier, locked, under_construction, construction_time, 
                          unlock_condition_from_level, unlock_condition_from_previous_environment,
                          unlock_available FROM environment WHERE locked = 1 AND map_id = 0''')
environment_info_fetched = USER_DB_CURSOR.fetchall()
for info in environment_info_fetched:
    CONSTRUCTION_STATE_MATRIX[PASSENGER_MAP][ENVIRONMENT][info[0]] = [bool(info[1]), bool(info[2]), info[3],
                                                                      bool(info[4]), bool(info[5]), 1, bool(info[6])]
    CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level FROM environment_config 
                                WHERE tier = ? AND map_id = 0''', (info[0], ))
    CONSTRUCTION_STATE_MATRIX[PASSENGER_MAP][ENVIRONMENT][info[0]].extend(CONFIG_DB_CURSOR.fetchone())

MAP_SWITCHER_STATE_MATRIX = [[], []]
for m in (PASSENGER_MAP, FREIGHT_MAP):
    USER_DB_CURSOR.execute('''SELECT locked FROM map_progress WHERE map_id = ?''', (m, ))
    MAP_SWITCHER_STATE_MATRIX[m].append(bool(USER_DB_CURSOR.fetchone()[0]))
    CONFIG_DB_CURSOR.execute('''SELECT level_required, price FROM map_progress_config WHERE map_id = ?''', (m, ))
    MAP_SWITCHER_STATE_MATRIX[m].extend(CONFIG_DB_CURSOR.fetchone())


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    USER_DB_CONNECTION.commit()
    with open(__user_db_full_path, 'rb') as f:
        data1 = f.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data1[::3] + data1[1::3] + data1[2::3]).hexdigest())
