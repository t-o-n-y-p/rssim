from database import *


@final
class ModelV2:
    def __init__(self):
        self._game_paused = True
        self._log_options = self._get_log_options()
        self._i18n = self._get_i18n()
        self._notification_settings = self._get_notification_settings()
        self._graphics = self._get_graphics()
        self._map_position_settings = self._get_map_position_settings()
        self._game_progress = self._get_game_progress()
        self._map_progress = self._get_map_progress()
        self._epoch_timestamp = self._get_epoch_timestamp()
        self._constructor = self._get_constructor()
        self._scheduler = self._get_scheduler()
        self._base_schedule = self._get_base_schedule()
        self._trains = self._get_trains()
        self._signals = self._get_signals()
        self._train_routes = self._get_train_routes()
        self._switches = self._get_switches()
        self._crossovers = self._get_crossovers()
        self._tracks = self._get_tracks()
        self._environment = self._get_environment()
        self._shops = self._get_shops()
        self._shop_stages = self._get_shop_stages()
        self._bonus_codes = self._get_bonus_codes()
        self._version = self._get_version()

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

    # --------------------------------------------------------------------------------------------------------------
    # Methods for saving the player progress to the database
    # --------------------------------------------------------------------------------------------------------------

    def _set_game_progress(self):
        USER_DB_CURSOR.execute(
            '''UPDATE game_progress SET level = ?, exp = ?, money = ?, money_target = ?, exp_multiplier = ?, 
            exp_bonus_multiplier = ?, money_bonus_multiplier = ?, construction_time_bonus_multiplier = ?''',
            (self._game_progress[GAME_PROGRESS_LEVEL], self._game_progress[GAME_PROGRESS_EXP],
             self._game_progress[GAME_PROGRESS_MONEY], self._game_progress[GAME_PROGRESS_MONEY_TARGET],
             self._game_progress[GAME_PROGRESS_EXP_MULTIPLIER],
             self._game_progress[GAME_PROGRESS_EXP_BONUS_MULTIPLIER],
             self._game_progress[GAME_PROGRESS_MONEY_BONUS_MULTIPLIER],
             self._game_progress[GAME_PROGRESS_CONSTRUCTION_TIME_BONUS_MULTIPLIER])
        )

    def _set_map_progress(self):
        for m in self._map_progress:
            USER_DB_CURSOR.execute(
                '''UPDATE map_progress SET locked = ?, unlocked_tracks = ?, unlocked_environment = ?, 
                min_supported_cars_by_direction = ?, unlocked_car_collections = ?, entry_locked_state = ?
                WHERE map_id = ?''',
                (m[MAP_PROGRESS_LOCKED], m[MAP_PROGRESS_UNLOCKED_TRACKS], m[MAP_PROGRESS_UNLOCKED_ENVIRONMENT],
                 '|'.join([','.join(str(c) for c in d) for d in m[MAP_PROGRESS_MIN_SUPPORTED_CARS_BY_DIRECTION]]),
                 ','.join(str(c) for c in m[MAP_PROGRESS_UNLOCKED_CAR_COLLECTIONS]),
                 ','.join(str(t) for t in m[MAP_PROGRESS_ENTRY_LOCKED_STATE]), m[MAP_PROGRESS_MAP_ID]
                 )
            )

    def _set_epoch_timestamp(self):
        USER_DB_CURSOR.execute(
            '''UPDATE epoch_timestamp SET game_time = ?, game_time_fraction = ?''',
            (self._epoch_timestamp[EPOCH_TIMESTAMP_GAME_TIME],
             self._epoch_timestamp[EPOCH_TIMESTAMP_GAME_TIME_FRACTION])
        )

    def _set_constructor(self):
        for c in self._constructor:
            USER_DB_CURSOR.execute(
                '''UPDATE constructor SET money_target_activated = ?, money_target_cell_position = ? 
                WHERE map_id = ?''',
                (c[CONSTRUCTOR_MONEY_TARGET_ACTIVATED],
                 ','.join(str(p) for p in c[CONSTRUCTOR_MONEY_TARGET_CELL_POSITION]), c[CONSTRUCTOR_MAP_ID])
            )

    def _set_scheduler(self):
        for s in self._scheduler:
            USER_DB_CURSOR.execute(
                '''UPDATE scheduler SET train_counter = ?, next_cycle_start_time = ?, entry_busy_state = ? 
                WHERE map_id = ?''',
                (s[SCHEDULER_TRAIN_COUNTER], s[SCHEDULER_NEXT_CYCLE_START_TIME],
                 ','.join(str(t) for t in s[SCHEDULER_ENTRY_BUSY_STATE]), s[SCHEDULER_MAP_ID])
            )

    def _set_base_schedule(self):
        USER_DB_CURSOR.execute('''DELETE FROM base_schedule''')
        USER_DB_CURSOR.executemany(
            '''INSERT INTO base_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', self._base_schedule
        )

    def _set_trains(self):
        USER_DB_CURSOR.execute('''DELETE FROM trains''')
        for t in self._trains:
            USER_DB_CURSOR.execute(
                '''INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (t[TRAINS_MAP_ID], t[TRAINS_TRAIN_ID], t[TRAINS_CARS], t[TRAINS_TRAIN_ROUTE_TRACK_NUMBER],
                 t[TRAINS_TRAIN_ROUTE_TYPE], t[TRAINS_STATE], t[TRAINS_DIRECTION], t[TRAINS_NEW_DIRECTION],
                 t[TRAINS_CURRENT_DIRECTION], t[TRAINS_SPEED_STATE], t[TRAINS_SPEED_STATE_TIME], t[TRAINS_PRIORITY],
                 t[TRAINS_BOARDING_TIME], t[TRAINS_EXP], t[TRAINS_MONEY],
                 ','.join(str(p) for p in t[TRAINS_CARS_POSITION])
                 if len(t[TRAINS_CARS_POSITION]) > 0
                 else None,
                 '|'.join([','.join(str(p) for p in c) for c in t[TRAINS_CARS_POSITION_ABS]])
                 if len(t[TRAINS_CARS_POSITION_ABS]) > 0
                 else None,
                 t[TRAINS_STOP_POINT], t[TRAINS_DESTINATION_POINT], t[TRAINS_CAR_IMAGE_COLLECTION],
                 t[TRAINS_SWITCH_DIRECTION_REQUIRED])
            )

    def _set_signals(self):
        USER_DB_CURSOR.execute('''DELETE FROM signals''')
        USER_DB_CURSOR.executemany('''INSERT INTO signals VALUES (?, ?, ?, ?, ?)''', self._signals)

    def _set_train_routes(self):
        for r in self._train_routes:
            USER_DB_CURSOR.execute(
                '''UPDATE train_routes SET opened = ?, last_opened_by = ?, current_checkpoint = ?, priority = ?, 
                cars = ?, train_route_section_busy_state = ? WHERE track = ? AND train_route = ? AND map_id = ?''',
                (r[TRAIN_ROUTES_OPENED], r[TRAIN_ROUTES_LAST_OPENED_BY], r[TRAIN_ROUTES_CURRENT_CHECKPOINT],
                 r[TRAIN_ROUTES_PRIORITY], r[TRAIN_ROUTES_CARS],
                 ','.join(str(t) for t in r[TRAIN_ROUTES_TRAIN_ROUTE_SECTION_BUSY_STATE]),
                 r[TRAIN_ROUTES_TRACK], r[TRAIN_ROUTES_TRAIN_ROUTE], r[TRAIN_ROUTES_MAP_ID])
            )

    def _set_switches(self):
        USER_DB_CURSOR.execute('''DELETE FROM switches''')
        USER_DB_CURSOR.executemany('''INSERT INTO switches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', self._switches)

    def _set_crossovers(self):
        USER_DB_CURSOR.execute('''DELETE FROM crossovers''')
        USER_DB_CURSOR.executemany(
            '''INSERT INTO crossovers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            self._crossovers
        )

    def _set_tracks(self):
        USER_DB_CURSOR.execute('''DELETE FROM tracks''')
        USER_DB_CURSOR.executemany('''INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', self._tracks)

    def _set_environment(self):
        USER_DB_CURSOR.execute('''DELETE FROM environment''')
        USER_DB_CURSOR.executemany('''INSERT INTO environment VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', self._environment)

    def _set_shops(self):
        USER_DB_CURSOR.execute('''DELETE FROM shops''')
        USER_DB_CURSOR.executemany('''INSERT INTO shops VALUES (?, ?, ?, ?, ?)''', self._shops)

    def _set_shop_stages(self):
        USER_DB_CURSOR.execute('''DELETE FROM shop_stages''')
        USER_DB_CURSOR.executemany('''INSERT INTO shop_stages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', self._shop_stages)

    def _set_bonus_codes(self):
        USER_DB_CURSOR.execute('''DELETE FROM bonus_codes''')
        USER_DB_CURSOR.executemany('''INSERT INTO bonus_codes VALUES (?, ?, ?, ?, ?)''', self._bonus_codes)

    # --------------------------------------------------------------------------------------------------------------
    # Handlers for immediate commit (settings, fullscreen mode, bonus code abuse, etc.)
    # --------------------------------------------------------------------------------------------------------------

    @staticmethod
    def on_i18n_current_locale_update(i18n_current_locale):
        USER_DB_CURSOR.execute('''UPDATE i18n SET current_locale = ?''', (i18n_current_locale, ))
        on_commit()
        # call view model event

    @staticmethod
    def on_i18n_clock_24h_update(i18n_clock_24h):
        USER_DB_CURSOR.execute('''UPDATE i18n SET clock_24h = ?''', (i18n_clock_24h, ))
        on_commit()
        # call view model event

    @staticmethod
    def on_notification_settings_level_up_notification_enabled_update(
            notification_settings_level_up_notification_enabled
    ):
        USER_DB_CURSOR.execute(
            '''UPDATE notification_settings SET level_up_notification_enabled = ?''',
            notification_settings_level_up_notification_enabled
        )
        on_commit()
        # call view model event
