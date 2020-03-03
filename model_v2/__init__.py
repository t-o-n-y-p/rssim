from database import *


@final
class ModelV2:
    def __init__(self):
        self.view_model = None
        self.game_paused = True
        self.log_options = self._get_log_options()
        self.i18n = self._get_i18n()
        self.notification_settings = self._get_notification_settings()
        self.graphics = self._get_graphics()
        self.map_position_settings = self._get_map_position_settings()
        self.game_progress = self._get_game_progress()
        self.map_progress = self._get_map_progress()
        self.epoch_timestamp = self._get_epoch_timestamp()
        self.constructor = self._get_constructor()
        self.scheduler = self._get_scheduler()
        self.base_schedule = self._get_base_schedule()
        self.trains = self._get_trains()
        self.signals = self._get_signals()
        self.train_routes = self._get_train_routes()
        self.switches = self._get_switches()
        self.crossovers = self._get_crossovers()
        self.tracks = self._get_tracks()
        self.environment = self._get_environment()
        self.shops = self._get_shops()
        self.shop_stages = self._get_shop_stages()
        self.bonus_codes = self._get_bonus_codes()
        self.version = self._get_version()

    # --------------------------------------------------------------------------------------------------------------
    # Methods for reading the player progress database
    # --------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_log_options():
        USER_DB_CURSOR.execute('''SELECT * FROM log_options''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_i18n():
        USER_DB_CURSOR.execute('''SELECT * FROM i18n''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_notification_settings():
        USER_DB_CURSOR.execute('''SELECT * FROM notification_settings''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_graphics():
        USER_DB_CURSOR.execute('''SELECT * FROM graphics''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_map_position_settings():
        USER_DB_CURSOR.execute('''SELECT * FROM map_position_settings''')
        return [
            [
                m[MAP_POSITION_SETTINGS_MAP_ID],
                [int(p) for p in m[MAP_POSITION_SETTINGS_LAST_KNOWN_BASE_OFFSET].split(',')],
                m[MAP_POSITION_SETTINGS_LAST_KNOWN_ZOOM]
            ] for m in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_game_progress():
        USER_DB_CURSOR.execute('''SELECT * FROM game_progress''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_map_progress():
        USER_DB_CURSOR.execute('''SELECT * FROM map_progress''')
        return [
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

    @staticmethod
    def _get_epoch_timestamp():
        USER_DB_CURSOR.execute('''SELECT * FROM epoch_timestamp''')
        return list(USER_DB_CURSOR.fetchall()[0])

    @staticmethod
    def _get_constructor():
        USER_DB_CURSOR.execute('''SELECT * FROM constructor''')
        return [
            [
                m[CONSTRUCTOR_MAP_ID],
                m[CONSTRUCTOR_MONEY_TARGET_ACTIVATED],
                [int(p) for p in m[CONSTRUCTOR_MONEY_TARGET_CELL_POSITION].split(',')]
            ] for m in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_scheduler():
        USER_DB_CURSOR.execute('''SELECT * FROM scheduler''')
        return [
            [
                m[SCHEDULER_MAP_ID],
                m[SCHEDULER_TRAIN_COUNTER],
                m[SCHEDULER_NEXT_CYCLE_START_TIME],
                [int(s) for s in m[SCHEDULER_ENTRY_BUSY_STATE].split(',')]
            ] for m in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_base_schedule():
        USER_DB_CURSOR.execute('''SELECT * FROM base_schedule''')
        return [
            list(t) for t in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_trains():
        USER_DB_CURSOR.execute('''SELECT * FROM trains''')
        return [
            [
                t[TRAINS_MAP_ID],
                t[TRAINS_TRAIN_ID],
                t[TRAINS_CARS],
                t[TRAINS_TRAIN_ROUTE_TRACK_NUMBER],
                t[TRAINS_TRAIN_ROUTE_TYPE],
                t[TRAINS_STATE],
                t[TRAINS_DIRECTION],
                t[TRAINS_NEW_DIRECTION],
                t[TRAINS_CURRENT_DIRECTION],
                t[TRAINS_SPEED_STATE],
                t[TRAINS_SPEED_STATE_TIME],
                t[TRAINS_PRIORITY],
                t[TRAINS_BOARDING_TIME],
                t[TRAINS_EXP],
                t[TRAINS_MONEY],
                [
                    float(p) for p in t[TRAINS_CARS_POSITION].split(',')
                ] if t[TRAINS_CARS_POSITION] is not None
                else [],
                [
                    [float(p) for p in s.split(',')] for s in t[TRAINS_CARS_POSITION_ABS].split('|')
                ] if t[TRAINS_CARS_POSITION_ABS] is not None
                else [],
                t[TRAINS_STOP_POINT],
                t[TRAINS_DESTINATION_POINT],
                t[TRAINS_CAR_IMAGE_COLLECTION],
                t[TRAINS_SWITCH_DIRECTION_REQUIRED]
            ] for t in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_signals():
        USER_DB_CURSOR.execute('''SELECT * FROM signals''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_train_routes():
        USER_DB_CURSOR.execute('''SELECT * FROM train_routes''')
        return [
            [
                r[TRAIN_ROUTES_MAP_ID],
                r[TRAIN_ROUTES_TRACK],
                r[TRAIN_ROUTES_TRAIN_ROUTE],
                r[TRAIN_ROUTES_OPENED],
                r[TRAIN_ROUTES_LAST_OPENED_BY],
                r[TRAIN_ROUTES_CURRENT_CHECKPOINT],
                r[TRAIN_ROUTES_PRIORITY],
                r[TRAIN_ROUTES_CARS],
                [int(s) for s in r[TRAIN_ROUTES_TRAIN_ROUTE_SECTION_BUSY_STATE].split(',')]
            ] for r in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_switches():
        USER_DB_CURSOR.execute('''SELECT * FROM switches''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_crossovers():
        USER_DB_CURSOR.execute('''SELECT * FROM crossovers''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_tracks():
        USER_DB_CURSOR.execute('''SELECT * FROM tracks''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_environment():
        USER_DB_CURSOR.execute('''SELECT * FROM environment''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_shops():
        USER_DB_CURSOR.execute('''SELECT * FROM shops''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_shop_stages():
        USER_DB_CURSOR.execute('''SELECT * FROM shop_stages''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_bonus_codes():
        USER_DB_CURSOR.execute('''SELECT * FROM bonus_codes''')
        return [
            list(s) for s in USER_DB_CURSOR.fetchall()
        ]

    @staticmethod
    def _get_version():
        USER_DB_CURSOR.execute('''SELECT * FROM version''')
        return list(USER_DB_CURSOR.fetchall()[0])
