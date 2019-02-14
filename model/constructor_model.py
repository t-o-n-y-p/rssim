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
        self.logger.info('START INIT')
        self.track_state_matrix = {}
        self.cached_unlocked_tracks = []
        self.user_db_cursor.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_track, 
                                       unlock_condition_from_environment, unlock_available FROM tracks 
                                       WHERE locked = 1''')
        track_info_fetched = self.user_db_cursor.fetchall()
        self.logger.debug(f'track_info_fetched: {track_info_fetched}')
        for info in track_info_fetched:
            self.track_state_matrix[info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]), bool(info[5]),
                                                bool(info[6]), bool(info[7])]
            self.logger.debug(f'track {info[0]} info: {self.track_state_matrix[info[0]]}')
            self.config_db_cursor.execute('SELECT price, level FROM track_config WHERE track_number = ?', (info[0], ))
            self.track_state_matrix[info[0]].extend(self.config_db_cursor.fetchone())
            self.logger.debug(f'extended track {info[0]} info: {self.track_state_matrix[info[0]]}')
            self.logger.debug(f'track state matrix: {self.track_state_matrix}')

        self.user_db_cursor.execute('SELECT money FROM game_progress')
        self.money = self.user_db_cursor.fetchone()[0]
        self.logger.debug(f'money: {self.money}')
        self.logger.info('END INIT')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model. Does not activate the view because constructor screen is not opened by default.
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
        Updates bank account state and activates the Constructor view.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_update_money(self.money, self.track_state_matrix)
        self.view.on_activate()
        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_update_time(self, game_time):
        """
        Decreases construction time for all tracks under construction.
        When construction time reaches 0, track is unlocked.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
        # unlocked_track stores track number if some track was unlocked and 0 otherwise
        unlocked_track = 0
        self.logger.debug(f'unlocked_track: {unlocked_track}')
        for track in self.track_state_matrix:
            self.logger.debug(f'track {track} under construction: {self.track_state_matrix[track][UNDER_CONSTRUCTION]}')
            if self.track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.track_state_matrix[track][CONSTRUCTION_TIME] -= 1
                self.logger.debug(f'construction_time: {self.track_state_matrix[track][CONSTRUCTION_TIME]}')
                self.view.on_update_live_track_state(self.track_state_matrix, track)
                if self.track_state_matrix[track][CONSTRUCTION_TIME] == 0:
                    unlocked_track = track
                    self.logger.debug(f'unlocked_track: {unlocked_track}')
                    self.track_state_matrix[track][UNDER_CONSTRUCTION] = False
                    self.logger.debug(f'under construction: {self.track_state_matrix[track][UNDER_CONSTRUCTION]}')
                    self.track_state_matrix[track][LOCKED] = False
                    self.logger.debug(f'locked: {self.track_state_matrix[track][LOCKED]}')
                    self.controller.parent_controller.on_unlock_track(track)
                    # track is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tracks.append(track)
                    self.logger.debug(f'cached_unlocked_tracks: {self.cached_unlocked_tracks}')
                    # if there are more tracks to unlock, unlock condition for the next track is met
                    if track < MAXIMUM_TRACK_NUMBER:
                        self.logger.debug('track limit is not reached')
                        self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
                        self.logger.debug('track {} unlock condition from previous track: {}'
                                          .format(track + 1,
                                                  self.track_state_matrix[track + 1][
                                                      UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
                        # if all three conditions are met for the next track, it becomes available for construction
                        self.logger.debug('track {} unlock condition from level: {}'
                                          .format(track + 1,
                                                  self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL]))
                        self.logger.debug('track {} unlock condition from environment: {}'
                                          .format(track + 1,
                                                  self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_ENVIRONMENT])
                                          )
                        if self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL] \
                                and self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                            self.logger.debug('all three conditions are met')
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
                            self.logger.debug('track {} unlock condition from previous track: {}'
                                              .format(track + 1,
                                                      self.track_state_matrix[track + 1][
                                                                                UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL] = False
                            self.logger.debug('track {} unlock condition from level: {}'
                                              .format(track + 1,
                                                      self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_LEVEL]))
                            self.track_state_matrix[track + 1][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
                            self.logger.debug('track {} unlock condition from environment: {}'
                                              .format(track + 1,
                                                      self.track_state_matrix[track + 1][
                                                          UNLOCK_CONDITION_FROM_ENVIRONMENT])
                                              )
                            self.track_state_matrix[track + 1][UNLOCK_AVAILABLE] = True
                            self.logger.debug('track {} unlock available: {}'
                                              .format(track + 1, self.track_state_matrix[track + 1][UNLOCK_AVAILABLE]))

                        self.view.on_update_live_track_state(self.track_state_matrix, track + 1)
                    else:
                        self.logger.debug('no more tracks to unlock')

                    self.view.on_unlock_track_live(track)

        self.logger.debug(f'unlocked_track: {unlocked_track}')
        self.logger.debug(f'track state matrix length: {len(self.track_state_matrix)}')
        if unlocked_track > 0:
            self.logger.debug(f'removing track {unlocked_track}')
            self.track_state_matrix.pop(unlocked_track)
            self.logger.debug(f'track state matrix length: {len(self.track_state_matrix)}')

        self.view.on_update_track_state(self.track_state_matrix, game_time)
        self.logger.info('END ON_UPDATE_TIME')

    def on_save_state(self):
        """
        Saves track state matrix to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        # if some tracks were unlocked since last time the game progress was saved,
        # they are not listed in track state matrix anymore, so their state is updated separately
        self.logger.debug(f'cached_unlocked_tracks: {self.cached_unlocked_tracks}')
        for track in self.cached_unlocked_tracks:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = 0, under_construction = 0, 
                                           construction_time = 0, unlock_condition_from_level = 0, 
                                           unlock_condition_from_previous_track = 0, 
                                           unlock_condition_from_environment = 0, unlock_available = 0 
                                           WHERE track_number = ?''', (track, ))
            self.logger.debug(f'track {track} state saved successfully')

        self.cached_unlocked_tracks = []
        self.logger.debug(f'cached_unlocked_tracks: {self.cached_unlocked_tracks}')
        # locked tracks state is saved from track_state_matrix the same way it was read
        self.logger.debug(f'track_state_matrix: {self.track_state_matrix}')
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
            self.logger.debug(f'track {track} state saved: {self.track_state_matrix[track]}')

        self.logger.info('END ON_SAVE_STATE')

    def on_level_up(self, level):
        """
        Checks if there are some tracks to be unlocked when player hits new level and adjusts its state properly.

        :param level:                   new level value
        """
        self.logger.info('START ON_LEVEL_UP')
        # determines if some tracks require level which was just hit
        self.config_db_cursor.execute('SELECT track_number FROM track_config WHERE level = ?', (level, ))
        raw_tracks = self.config_db_cursor.fetchall()
        tracks_parsed = []
        for i in raw_tracks:
            tracks_parsed.append(i[0])

        self.logger.debug(f'tracks_parsed: {tracks_parsed}')

        # adjusts "unlock_from_level" condition for all tracks
        for track in tracks_parsed:
            self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = True
            self.logger.debug('track {} unlock condition from level: {}'
                              .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]))
            self.logger.debug('track {} unlock condition from previous track: {}'
                              .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
            self.logger.debug('track {} unlock condition from environment: {}'
                              .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]))
            # if all three conditions are met, track is available for construction
            if self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                    and self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                self.logger.debug('all three conditions met')
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL] = False
                self.logger.debug('track {} unlock condition from level: {}'
                                  .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]))
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
                self.logger.debug('track {} unlock condition from previous track: {}'
                                  .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
                self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
                self.logger.debug('track {} unlock condition from environment: {}'
                                  .format(track, self.track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]))
                self.track_state_matrix[track][UNLOCK_AVAILABLE] = True
                self.logger.debug('track {} unlock available: {}'
                                  .format(track, self.track_state_matrix[track][UNLOCK_AVAILABLE]))

            self.view.on_update_live_track_state(self.track_state_matrix, track)

        self.logger.info('END ON_LEVEL_UP')

    def on_put_track_under_construction(self, track):
        """
        Notifies Game controller to take money from the player and puts track under construction.

        :param track:                   track number
        """
        self.logger.info('START ON_PUT_TRACK_UNDER_CONSTRUCTION')
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.track_state_matrix[track][PRICE])
        self.track_state_matrix[track][UNLOCK_AVAILABLE] = False
        self.logger.debug('track {} unlock available: {}'
                          .format(track, self.track_state_matrix[track][UNLOCK_AVAILABLE]))
        self.track_state_matrix[track][UNDER_CONSTRUCTION] = True
        self.logger.debug('track {} under construction: {}'
                          .format(track, self.track_state_matrix[track][UNDER_CONSTRUCTION]))
        self.view.on_update_live_track_state(self.track_state_matrix, track)
        self.logger.info('END ON_PUT_TRACK_UNDER_CONSTRUCTION')

    @maximum_money_not_reached
    def on_add_money(self, money):
        """
        Updates bank account state change when user gains money. Notifies the view about state change.

        :param money:                   amount of money gained
        """
        self.logger.info('START ON_ADD_MONEY')
        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT

        self.logger.debug(f'money: {self.money}')
        self.view.on_update_money(self.money, self.track_state_matrix)
        self.logger.info('END ON_ADD_MONEY')

    def on_pay_money(self, money):
        """
        Updates bank account state change when user spends money. Notifies the view about state change.

        :param money:                   amount of money spent
        """
        self.logger.info('START ON_PAY_MONEY')
        self.money -= money
        self.logger.debug(f'money: {self.money}')
        self.view.on_update_money(self.money, self.track_state_matrix)
        self.logger.info('END ON_PAY_MONEY')
