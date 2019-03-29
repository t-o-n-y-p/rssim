from logging import getLogger

from model import *


class ConstructorModel(Model):
    """
    Implements Constructor model.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.constructor.model'))
        self.construction_state_matrix = [{}, {}]
        self.cached_unlocked_tracks = []
        self.cached_unlocked_tiers = []
        self.user_db_cursor.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_track, 
                                       unlock_condition_from_environment, unlock_available FROM tracks 
                                       WHERE locked = 1''')
        track_info_fetched = self.user_db_cursor.fetchall()
        for info in track_info_fetched:
            self.construction_state_matrix[TRACKS][info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]),
                                                               bool(info[5]), bool(info[6]), bool(info[7])]
            self.config_db_cursor.execute('''SELECT price, level, environment_tier FROM track_config 
                                             WHERE track_number = ?''', (info[0], ))
            self.construction_state_matrix[TRACKS][info[0]].extend(self.config_db_cursor.fetchone())

        self.user_db_cursor.execute('''SELECT tier, locked, under_construction, construction_time, 
                                       unlock_condition_from_level, unlock_condition_from_previous_environment,
                                       unlock_available FROM environment WHERE locked = 1''')
        environment_info_fetched = self.user_db_cursor.fetchall()
        for info in environment_info_fetched:
            self.construction_state_matrix[ENVIRONMENT][info[0]] = [bool(info[1]), bool(info[2]), info[3],
                                                                    bool(info[4]), bool(info[5]), 1, bool(info[6])]
            self.config_db_cursor.execute('SELECT price, level FROM environment_config WHERE tier = ?', (info[0], ))
            self.construction_state_matrix[ENVIRONMENT][info[0]].extend(self.config_db_cursor.fetchone())

        self.user_db_cursor.execute('SELECT money FROM game_progress')
        self.money = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT money_target_activated FROM graphics')
        self.money_target_activated = bool(self.user_db_cursor.fetchone()[0])
        self.user_db_cursor.execute('SELECT money_target_cell_position FROM graphics')
        self.money_target_cell_position = list(map(int, self.user_db_cursor.fetchone()[0].split(',')))

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
        self.view.on_update_construction_state(self.construction_state_matrix)
        self.view.on_update_money(self.money)
        self.view.on_activate()

    def on_update_time(self, game_time):
        """
        Decreases construction time for all tracks under construction.
        When construction time reaches 0, track is unlocked.

        :param game_time:               current in-game time
        """
        # unlocked_track stores track number if some track was unlocked and 0 otherwise
        unlocked_track = 0
        for track in self.construction_state_matrix[TRACKS]:
            if self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION]:
                self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME] -= 1
                if self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME] == 0:
                    unlocked_track = track
                    self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION] = False
                    self.construction_state_matrix[TRACKS][track][LOCKED] = False
                    self.view.on_send_track_construction_completed_notification(track)
                    self.controller.parent_controller.on_unlock_track(track)
                    # track is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tracks.append(track)
                    # if there are more tracks to unlock, unlock condition for the next track is met
                    if track < MAXIMUM_TRACK_NUMBER:
                        self.construction_state_matrix[TRACKS][track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
                        # if all three conditions are met for the next track, it becomes available for construction
                        self.on_check_track_unlock_conditions(track + 1)

                    self.view.on_unlock_construction(TRACKS, track)

                self.view.on_update_construction_state(self.construction_state_matrix)

        if unlocked_track > 0:
            self.construction_state_matrix[TRACKS].pop(unlocked_track)
            if self.money_target_activated and self.money_target_cell_position[0] == TRACKS \
                    and self.money_target_cell_position[1] > 0:
                self.money_target_cell_position[1] -= 1

        # same for environment
        unlocked_tier = 0
        for tier in self.construction_state_matrix[ENVIRONMENT]:
            if self.construction_state_matrix[ENVIRONMENT][tier][UNDER_CONSTRUCTION]:
                self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME] -= 1
                if self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME] == 0:
                    unlocked_tier = tier
                    self.construction_state_matrix[ENVIRONMENT][tier][UNDER_CONSTRUCTION] = False
                    self.construction_state_matrix[ENVIRONMENT][tier][LOCKED] = False
                    self.view.on_send_environment_construction_completed_notification(tier)
                    self.controller.parent_controller.on_unlock_environment(tier)
                    # track is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tiers.append(tier)
                    # if there are more tracks to unlock, unlock condition for the next track is met
                    if tier < MAXIMUM_ENVIRONMENT_TIER:
                        self.construction_state_matrix[ENVIRONMENT][tier + 1][
                            UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] = True
                        # if all three conditions are met for the next track, it becomes available for construction
                        self.on_check_environment_unlock_conditions(tier + 1)

                    self.view.on_unlock_construction(ENVIRONMENT, tier)

                self.view.on_update_construction_state(self.construction_state_matrix)

        if unlocked_tier > 0:
            self.construction_state_matrix[ENVIRONMENT].pop(unlocked_tier)
            if self.money_target_activated and self.money_target_cell_position[0] == ENVIRONMENT \
                    and self.money_target_cell_position[1] > 0:
                self.money_target_cell_position[1] -= 1

    def on_save_state(self):
        """
        Saves track state matrix and money target flags to user progress database.
        """
        self.user_db_cursor.execute('UPDATE graphics SET money_target_activated = ?, money_target_cell_position = ?',
                                    (int(self.money_target_activated),
                                     ','.join(list(map(str, self.money_target_cell_position)))))
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
        for track in self.construction_state_matrix[TRACKS]:
            self.user_db_cursor.execute('''UPDATE tracks SET locked = ?, under_construction = ?, construction_time = ?, 
                                           unlock_condition_from_level = ?, unlock_condition_from_previous_track = ?, 
                                           unlock_condition_from_environment = ?, unlock_available = ? 
                                           WHERE track_number = ?''',
                                        tuple(
                                            map(int,
                                                (self.construction_state_matrix[TRACKS][track][LOCKED],
                                                 self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION],
                                                 self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME],
                                                 self.construction_state_matrix[TRACKS][track][
                                                     UNLOCK_CONDITION_FROM_LEVEL],
                                                 self.construction_state_matrix[TRACKS][track][
                                                     UNLOCK_CONDITION_FROM_PREVIOUS_TRACK],
                                                 self.construction_state_matrix[TRACKS][track][
                                                     UNLOCK_CONDITION_FROM_ENVIRONMENT],
                                                 self.construction_state_matrix[TRACKS][track][UNLOCK_AVAILABLE],
                                                 track)
                                                )
                                            )
                                        )

        # same for environment
        for tier in self.cached_unlocked_tiers:
            self.user_db_cursor.execute('''UPDATE environment SET locked = 0, under_construction = 0, 
                                           construction_time = 0, unlock_condition_from_level = 0, 
                                           unlock_condition_from_previous_environment = 0, 
                                           unlock_available = 0 WHERE tier = ?''', (tier, ))

        self.cached_unlocked_tiers = []
        for tier in self.construction_state_matrix[ENVIRONMENT]:
            self.user_db_cursor.execute('''UPDATE environment SET locked = ?, under_construction = ?, 
                                           construction_time = ?, unlock_condition_from_level = ?, 
                                           unlock_condition_from_previous_environment = ?, 
                                           unlock_available = ? WHERE tier = ?''',
                                        tuple(
                                            map(int,
                                                (self.construction_state_matrix[ENVIRONMENT][tier][LOCKED],
                                                 self.construction_state_matrix[ENVIRONMENT][tier][UNDER_CONSTRUCTION],
                                                 self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME],
                                                 self.construction_state_matrix[ENVIRONMENT][tier][
                                                     UNLOCK_CONDITION_FROM_LEVEL],
                                                 self.construction_state_matrix[ENVIRONMENT][tier][
                                                     UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT],
                                                 self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_AVAILABLE],
                                                 tier)
                                                )
                                            )
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
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = True
            # if all three conditions are met, track is available for construction
            self.on_check_track_unlock_conditions(track)

        if len(tracks_parsed) > 0:
            self.view.on_update_construction_state(self.construction_state_matrix)

        # same for environment
        self.config_db_cursor.execute('SELECT tier FROM environment_config WHERE level = ?', (level, ))
        raw_tiers = self.config_db_cursor.fetchall()
        tiers_parsed = []
        for i in raw_tiers:
            tiers_parsed.append(i[0])

        for tier in tiers_parsed:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = True
            self.on_check_environment_unlock_conditions(tier)

        if len(tiers_parsed) > 0:
            self.view.on_update_construction_state(self.construction_state_matrix)

    def on_put_under_construction(self, construction_type, entity_number):
        self.construction_state_matrix[construction_type][entity_number][UNLOCK_AVAILABLE] = False
        self.construction_state_matrix[construction_type][entity_number][UNDER_CONSTRUCTION] = True
        self.view.on_update_construction_state(self.construction_state_matrix)
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.construction_state_matrix[construction_type][entity_number][PRICE])

    @maximum_money_not_reached
    def on_add_money(self, money):
        """
        Updates bank account state change when user gains money. Notifies the view about state change.

        :param money:                   amount of money gained
        """
        self.money += money
        if self.money > MONEY_LIMIT:
            self.money = MONEY_LIMIT

        self.view.on_update_money(self.money)

    def on_pay_money(self, money):
        """
        Updates bank account state change when user spends money. Notifies the view about state change.

        :param money:                   amount of money spent
        """
        self.money -= money
        self.view.on_update_money(self.money)

    def on_check_track_unlock_conditions(self, track):
        """
        Checks if all 3 unlock conditions are met.
        If so, unlocks the track and notifies the view to send notification.

        :param track:                           track number to check
        """
        if self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_AVAILABLE] = True
            self.view.on_send_track_unlocked_notification(track)

    def on_check_environment_unlock_conditions(self, tier):
        """
        Checks if all 2 unlock conditions are met.
        If so, unlocks the tier and notifies the view to send notification.

        :param tier:                            environment tier to check
        """
        if self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] \
                and self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_AVAILABLE] = True
            self.view.on_send_environment_unlocked_notification(tier)

    def on_activate_money_target(self, construction_type, row):
        """
        Updates track_money_target_activated flag value.
        Notifies view that track money target was activated.

        :param construction_type:               column to activate money target: tracks or environment
        :param row:                             number of cell in a given column
        """
        self.money_target_activated = True
        self.money_target_cell_position = [construction_type, row]
        self.view.on_activate_money_target(construction_type, row)

    def on_deactivate_money_target(self):
        """
        Updates track_money_target_activated flag value.
        Notifies view that track money target was deactivated.
        """
        self.money_target_activated = False
        self.view.on_deactivate_money_target()
