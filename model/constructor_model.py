from logging import getLogger

from model import *


class ConstructorModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.constructor.model'))
        self.user_db_cursor.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_track, 
                                       unlock_condition_from_environment, unlock_available FROM tracks 
                                       WHERE locked = 1''')
        self.track_state_matrix = {}
        track_info_fetched = self.user_db_cursor.fetchall()
        for info in track_info_fetched:
            self.track_state_matrix[info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]), bool(info[5]),
                                                bool(info[6]), bool(info[7])]
            self.config_db_cursor.execute('SELECT price, level FROM track_config WHERE track_number = ?', (info[0], ))
            self.track_state_matrix[info[0]].extend(self.config_db_cursor.fetchone())

        self.user_db_cursor.execute('SELECT money FROM game_progress')
        self.money = self.user_db_cursor.fetchone()[0]
        self.cached_unlocked_tracks = []

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_update_money(self.money, self.track_state_matrix)
        self.view.on_activate()

    def on_update_time(self, game_time):
        unlocked_track = 0
        for track in self.track_state_matrix:
            if self.track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.track_state_matrix[track][CONSTRUCTION_TIME] -= 1
                self.view.on_update_live_track_state(self.track_state_matrix, track)
                if self.track_state_matrix[track][CONSTRUCTION_TIME] == 0:
                    unlocked_track = track
                    self.track_state_matrix[track][UNDER_CONSTRUCTION] = False
                    self.track_state_matrix[track][LOCKED] = False
                    self.controller.parent_controller.on_unlock_track(track)
                    self.cached_unlocked_tracks.append(track)
                    if track < 32:
                        self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
                        if self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL] \
                                and self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL] = False
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
                            self.track_state_matrix[track + 1][UNLOCK_AVAILABLE] = True

                        self.view.on_update_live_track_state(self.track_state_matrix, track + 1)

                    self.view.on_unlock_track_live(track)

        if unlocked_track > 0:
            self.track_state_matrix.pop(unlocked_track)

        self.view.on_update_track_state(self.track_state_matrix, game_time)

    def on_save_state(self):
        for track in self.cached_unlocked_tracks:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = 0, under_construction = 0, 
                                           construction_time = 0, unlock_condition_from_level = 0, 
                                           unlock_condition_from_previous_track = 0, 
                                           unlock_condition_from_environment = 0, unlock_available = 0 
                                           WHERE track_number = ?''', (track, ))

        self.cached_unlocked_tracks = []
        for track in self.track_state_matrix:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = ?, under_construction = ?, construction_time = ?, 
                                           unlock_condition_from_level = ?, unlock_condition_from_previous_track = ?, 
                                           unlock_condition_from_environment = ?, unlock_available = ? 
                                           WHERE track_number = ?''',
                                        (self.track_state_matrix[track][LOCKED],
                                         self.track_state_matrix[track][UNDER_CONSTRUCTION],
                                         self.track_state_matrix[track][CONSTRUCTION_TIME],
                                         self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL],
                                         self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK],
                                         self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT],
                                         self.track_state_matrix[track][UNLOCK_AVAILABLE], track)
                                        )

    def on_level_up(self, level):
        self.config_db_cursor.execute('SELECT track_number FROM track_config WHERE level = ?', (level, ))
        raw_tracks = self.config_db_cursor.fetchall()
        tracks_parsed = []
        for i in raw_tracks:
            tracks_parsed.append(i[0])

        for track in tracks_parsed:
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = True
            if self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                    and self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = False
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
                self.track_state_matrix[track][UNLOCK_AVAILABLE] = True

            self.view.on_update_live_track_state(self.track_state_matrix, track)

    def on_put_track_under_construction(self, track):
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.track_state_matrix[track][PRICE])
        self.track_state_matrix[track][UNLOCK_AVAILABLE] = False
        self.track_state_matrix[track][UNDER_CONSTRUCTION] = True
        self.view.on_update_live_track_state(self.track_state_matrix, track)

    @maximum_money_not_reached
    def on_add_money(self, money):
        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT

        self.view.on_update_money(self.money, self.track_state_matrix)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money, self.track_state_matrix)
