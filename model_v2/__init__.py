from database import *


@final
class ModelV2:
    def __init__(self):
        self.view_model = None
        USER_DB_CURSOR.execute('''SELECT * FROM log_options''')
        self.log_options = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM i18n''')
        self.i18n = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM notification_settings''')
        self.notification_settings = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM graphics''')
        self.graphics = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM map_position_settings''')
        self.map_position_settings = [
            [
                m[MAP_POSITION_SETTINGS_MAP_ID],
                [int(p) for p in m[MAP_POSITION_SETTINGS_LAST_KNOWN_BASE_OFFSET].split(',')],
                m[MAP_POSITION_SETTINGS_LAST_KNOWN_ZOOM]
            ] for m in USER_DB_CURSOR.fetchall()
        ]
        USER_DB_CURSOR.execute('''SELECT * FROM game_progress''')
        self.game_progress = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM map_progress''')
        self.map_progress = [
            [
                m[MAP_PROGRESS_MAP_ID],
                m[MAP_PROGRESS_LOCKED],
                m[MAP_PROGRESS_UNLOCKED_TRACKS],
                m[MAP_PROGRESS_UNLOCKED_ENVIRONMENT],
                [
                    [int(c) for c in s.split(',')] for s in m[MAP_PROGRESS_MIN_SUPPORTED_CARS_BY_DIRECTION].split('|')
                ],
                [int(c) for c in m[MAP_PROGRESS_UNLOCKED_CAR_COLLECTIONS].split(',')],
                [int(e) for e in m[MAP_PROGRESS_ENTRY_LOCKED_STATE].split(',')]
            ] for m in USER_DB_CURSOR.fetchall()
        ]
        USER_DB_CURSOR.execute('''SELECT * FROM epoch_timestamp''')
        self.epoch_timestamp = list(USER_DB_CURSOR.fetchall()[0])
        USER_DB_CURSOR.execute('''SELECT * FROM constructor''')
        self.constructor = [
            [
                m[CONSTRUCTOR_MAP_ID],
                m[CONSTRUCTOR_MONEY_TARGET_ACTIVATED],
                [int(p) for p in m[CONSTRUCTOR_MONEY_TARGET_CELL_POSITION].split(',')]
            ] for m in USER_DB_CURSOR.fetchall()
        ]
        USER_DB_CURSOR.execute('''SELECT * FROM scheduler''')
        self.scheduler = [
            [
                m[SCHEDULER_MAP_ID],
                m[SCHEDULER_TRAIN_COUNTER],
                m[SCHEDULER_NEXT_CYCLE_START_TIME],
                [int(s) for s in m[SCHEDULER_ENTRY_BUSY_STATE].split(',')]
            ] for m in USER_DB_CURSOR.fetchall()
        ]
        USER_DB_CURSOR.execute('''SELECT * FROM base_schedule''')
        self.base_schedule = [
            list(t) for t in USER_DB_CURSOR.fetchall()
        ]
