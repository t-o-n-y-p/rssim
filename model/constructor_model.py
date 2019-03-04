from logging import getLogger

from model import *


class ConstructorModel(Model):
    """
    Implements Constructor model.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            track_state_matrix                  table with all tracks state properties:
                                                property #0 indicates if track is locked
                                                property #1 indicates if track is under construction
                                                property #2 indicates construction time left
                                                property #3 indicates if unlock condition from level is met
                                                property #4 indicates if unlock condition from previous track is met
                                                property #5 indicates if unlock condition from environment is met
                                                property #6 indicates if all unlock conditions are met
                                                property #7 indicates track price
                                                property #8 indicates required level for this track
            money                               player bank account state
            cached_unlocked_tracks              stores unlocked track number to remove it from constructor later

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.constructor.model'))
        self.track_state_matrix = {}
        self.cached_unlocked_tracks = []
        self.user_db_cursor.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_track, 
                                       unlock_condition_from_environment, unlock_available FROM tracks 
                                       WHERE locked = 1''')
        track_info_fetched = self.user_db_cursor.fetchall()
        for info in track_info_fetched:
            self.track_state_matrix[info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]), bool(info[5]),
                                                bool(info[6]), bool(info[7])]
            self.config_db_cursor.execute('SELECT price, level FROM track_config WHERE track_number = ?', (info[0], ))
            self.track_state_matrix[info[0]].extend(self.config_db_cursor.fetchone())

        self.user_db_cursor.execute('SELECT money FROM game_progress')
        self.money = self.user_db_cursor.fetchone()[0]

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model. Does not activate the view because constructor screen is not opened by default.
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
        Updates bank account state and activates the Constructor view.
        """
        self.view.on_update_money(self.money, self.track_state_matrix)
        self.view.on_activate()

    def on_update_time(self, game_time):
        """
        Decreases construction time for all tracks under construction.
        When construction time reaches 0, track is unlocked.

        :param game_time:               current in-game time
        """
        # unlocked_track stores track number if some track was unlocked and 0 otherwise
        unlocked_track = 0
        for track in self.track_state_matrix:
            if self.track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.track_state_matrix[track][CONSTRUCTION_TIME] -= 1
                self.view.on_update_live_track_state(self.track_state_matrix, track)
                if self.track_state_matrix[track][CONSTRUCTION_TIME] == 0:
                    unlocked_track = track
                    self.track_state_matrix[track][UNDER_CONSTRUCTION] = False
                    self.track_state_matrix[track][LOCKED] = False
                    self.view.on_send_track_construction_completed_notification(track)
                    self.controller.parent_controller.on_unlock_track(track)
                    # track is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tracks.append(track)
                    # if there are more tracks to unlock, unlock condition for the next track is met
                    if track < MAXIMUM_TRACK_NUMBER:
                        self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
                        # if all three conditions are met for the next track, it becomes available for construction
                        self.on_check_unlock_conditions(track + 1)

                        self.view.on_update_live_track_state(self.track_state_matrix, track + 1)

                    self.view.on_unlock_track_live(track)

        if unlocked_track > 0:
            self.track_state_matrix.pop(unlocked_track)

        self.view.on_update_track_state(self.track_state_matrix, game_time)

    def on_save_state(self):
        """
        Saves track state matrix and money target flags to user progress database.
        """
        self.user_db_cursor.execute('UPDATE graphics SET track_money_target_activated = ?',
                                    (self.view.track_money_target_activated, ))
        # if some tracks were unlocked since last time the game progress was saved,
        # they are not listed in track state matrix anymore, so their state is updated separately
        for track in self.cached_unlocked_tracks:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = 0, under_construction = 0, 
                                           construction_time = 0, unlock_condition_from_level = 0, 
                                           unlock_condition_from_previous_track = 0, 
                                           unlock_condition_from_environment = 0, unlock_available = 0 
                                           WHERE track_number = ?''', (track, ))

        self.cached_unlocked_tracks = []
        # locked tracks state is saved from track_state_matrix the same way it was read
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
        """
        Checks if there are some tracks to be unlocked when player hits new level and adjusts its state properly.

        :param level:                   new level value
        """
        # determines if some tracks require level which was just hit
        self.config_db_cursor.execute('SELECT track_number FROM track_config WHERE level = ?', (level, ))
        raw_tracks = self.config_db_cursor.fetchall()
        tracks_parsed = []
        for i in raw_tracks:
            tracks_parsed.append(i[0])

        # adjusts "unlock_from_level" condition for all tracks
        for track in tracks_parsed:
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = True
            # if all three conditions are met, track is available for construction
            self.on_check_unlock_conditions(track)

            self.view.on_update_live_track_state(self.track_state_matrix, track)

    def on_put_track_under_construction(self, track):
        """
        Notifies Game controller to take money from the player and puts track under construction.

        :param track:                   track number
        """
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.track_state_matrix[track][PRICE])
        self.track_state_matrix[track][UNLOCK_AVAILABLE] = False
        self.track_state_matrix[track][UNDER_CONSTRUCTION] = True
        self.view.on_update_live_track_state(self.track_state_matrix, track)

    @maximum_money_not_reached
    def on_add_money(self, money):
        """
        Updates bank account state change when user gains money. Notifies the view about state change.

        :param money:                   amount of money gained
        """
        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT

        self.view.on_update_money(self.money, self.track_state_matrix)

    def on_pay_money(self, money):
        """
        Updates bank account state change when user spends money. Notifies the view about state change.

        :param money:                   amount of money spent
        """
        self.money -= money
        self.view.on_update_money(self.money, self.track_state_matrix)

    def on_check_unlock_conditions(self, track):
        """
        Checks if all 3 unlock conditions are met.
        If so, unlocks the track and notifies the view to send notification.

        :param track:                           track number to check
        """
        if self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                and self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                and self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]:
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
            self.track_state_matrix[track][UNLOCK_AVAILABLE] = True
            self.view.on_send_track_unlocked_notification(track)
