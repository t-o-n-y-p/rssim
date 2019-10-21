from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class ConstructorModel(Model):
    def __init__(self, map_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.constructor.model'))
        self.map_id = map_id
        USER_DB_CURSOR.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT level FROM game_progress')
        self.level = USER_DB_CURSOR.fetchone()[0]
        self.construction_state_matrix = [{}, {}]
        self.cached_unlocked_tracks = []
        self.cached_unlocked_tiers = []
        USER_DB_CURSOR.execute('''SELECT track_number, locked, under_construction, construction_time, 
                                  unlock_condition_from_level, unlock_condition_from_previous_track, 
                                  unlock_condition_from_environment, unlock_available FROM tracks 
                                  WHERE locked = 1 AND map_id = ?''', (self.map_id, ))
        track_info_fetched = USER_DB_CURSOR.fetchall()
        for info in track_info_fetched:
            self.construction_state_matrix[TRACKS][info[0]] = [bool(info[1]), bool(info[2]), info[3], bool(info[4]),
                                                               bool(info[5]), bool(info[6]), bool(info[7])]
            CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level, environment_tier FROM track_config 
                                        WHERE track_number = ? AND map_id = ?''', (info[0], self.map_id))
            self.construction_state_matrix[TRACKS][info[0]].extend(CONFIG_DB_CURSOR.fetchone())

        USER_DB_CURSOR.execute('''SELECT tier, locked, under_construction, construction_time, 
                                  unlock_condition_from_level, unlock_condition_from_previous_environment,
                                  unlock_available FROM environment WHERE locked = 1 AND map_id = ?''',
                               (self.map_id, ))
        environment_info_fetched = USER_DB_CURSOR.fetchall()
        for info in environment_info_fetched:
            self.construction_state_matrix[ENVIRONMENT][info[0]] = [bool(info[1]), bool(info[2]), info[3],
                                                                    bool(info[4]), bool(info[5]), 1, bool(info[6])]
            CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level FROM environment_config 
                                        WHERE tier = ? AND map_id = ?''',
                                     (info[0], self.map_id))
            self.construction_state_matrix[ENVIRONMENT][info[0]].extend(CONFIG_DB_CURSOR.fetchone())

        USER_DB_CURSOR.execute('SELECT money FROM game_progress')
        self.money = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT money_target_activated FROM constructor WHERE map_id = ?', (self.map_id, ))
        self.money_target_activated = bool(USER_DB_CURSOR.fetchone()[0])
        USER_DB_CURSOR.execute('SELECT money_target_cell_position FROM constructor WHERE map_id = ?',
                               (self.map_id, ))
        self.money_target_cell_position = list(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))

    def on_activate_view(self):
        remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
        for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
            self.view.on_update_construction_state(TRACKS, remaining_tracks[j])

        remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
        for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
            self.view.on_update_construction_state(ENVIRONMENT, remaining_tiers[j])

        self.view.on_update_money(self.money)
        self.view.on_activate()

    def on_update_time(self):
        self.game_time += 1
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
                    if track < MAXIMUM_TRACK_NUMBER[self.map_id]:
                        self.construction_state_matrix[TRACKS][track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
                        # if all three conditions are met for the next track, it becomes available for construction
                        self.on_check_track_unlock_conditions(track + 1)

                    self.view.on_unlock_construction(TRACKS, track)
                else:
                    self.view.on_update_construction_state(TRACKS, track, self.game_time)

        if unlocked_track > 0:
            self.construction_state_matrix[TRACKS].pop(unlocked_track)
            # if money target is activated for another track, cell position is updated
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
                    # tier is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tiers.append(tier)
                    # unlock condition from environment is made up
                    for track in self.construction_state_matrix[TRACKS]:
                        if self.construction_state_matrix[TRACKS][track][ENVIRONMENT_REQUIRED] == tier:
                            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = True
                            self.on_check_track_unlock_conditions(track)
                            self.view.on_update_construction_state(TRACKS, track)

                    # if there are more tiers to unlock, unlock condition for the next tier is met
                    if tier < MAXIMUM_ENVIRONMENT_TIER[self.map_id]:
                        self.construction_state_matrix[ENVIRONMENT][tier + 1][
                            UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] = True
                        # if all 2 conditions are met for the next tier, it becomes available for construction
                        self.on_check_environment_unlock_conditions(tier + 1)

                    self.view.on_unlock_construction(ENVIRONMENT, tier)
                else:
                    self.view.on_update_construction_state(ENVIRONMENT, tier, self.game_time)

        if unlocked_tier > 0:
            self.construction_state_matrix[ENVIRONMENT].pop(unlocked_tier)
            # if money target is activated for another tier, cell position is updated
            if self.money_target_activated and self.money_target_cell_position[0] == ENVIRONMENT \
                    and self.money_target_cell_position[1] > 0:
                self.money_target_cell_position[1] -= 1

    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE constructor SET money_target_activated = ?, money_target_cell_position = ? 
                                  WHERE map_id = ?''',
                               (int(self.money_target_activated),
                                ','.join(list(map(str, self.money_target_cell_position))), self.map_id))
        # if some tracks were unlocked since last time the game progress was saved,
        # they are not listed in track state matrix anymore, so their state is updated separately
        for track in self.cached_unlocked_tracks:
            USER_DB_CURSOR.execute('''UPDATE tracks SET locked = 0, under_construction = 0, 
                                      construction_time = 0, unlock_condition_from_level = 0, 
                                      unlock_condition_from_previous_track = 0, 
                                      unlock_condition_from_environment = 0, unlock_available = 0 
                                      WHERE track_number = ? AND map_id = ?''', (track, self.map_id))

        self.cached_unlocked_tracks = []
        # locked tracks state is saved from track_state_matrix the same way it was read
        for track in self.construction_state_matrix[TRACKS]:
            USER_DB_CURSOR.execute('''UPDATE tracks SET locked = ?, under_construction = ?, construction_time = ?, 
                                      unlock_condition_from_level = ?, unlock_condition_from_previous_track = ?, 
                                      unlock_condition_from_environment = ?, unlock_available = ? 
                                      WHERE track_number = ? AND map_id = ?''',
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
                                            track, self.map_id)
                                           )
                                        )
                                   )

        # same for environment
        for tier in self.cached_unlocked_tiers:
            USER_DB_CURSOR.execute('''UPDATE environment SET locked = 0, under_construction = 0, 
                                      construction_time = 0, unlock_condition_from_level = 0, 
                                      unlock_condition_from_previous_environment = 0, 
                                      unlock_available = 0 WHERE tier = ? AND map_id = ?''', (tier, self.map_id))

        self.cached_unlocked_tiers = []
        for tier in self.construction_state_matrix[ENVIRONMENT]:
            USER_DB_CURSOR.execute('''UPDATE environment SET locked = ?, under_construction = ?, 
                                      construction_time = ?, unlock_condition_from_level = ?, 
                                      unlock_condition_from_previous_environment = ?, 
                                      unlock_available = ? WHERE tier = ? AND map_id = ?''',
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
                                            tier, self.map_id)
                                           )
                                        )
                                   )

    def on_level_up(self):
        self.level += 1
        # determines if some tracks require level which was just hit
        CONFIG_DB_CURSOR.execute('SELECT track_number FROM track_config WHERE level = ? AND map_id = ?',
                                 (self.level, self.map_id))
        raw_tracks = CONFIG_DB_CURSOR.fetchall()
        tracks_parsed = []
        for i in raw_tracks:
            tracks_parsed.append(i[0])

        # adjusts "unlock_from_level" condition for all tracks
        for track in tracks_parsed:
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = True
            # if all three conditions are met, track is available for construction
            self.on_check_track_unlock_conditions(track)
            self.view.on_update_construction_state(TRACKS, track)

        # same for environment
        CONFIG_DB_CURSOR.execute('SELECT tier FROM environment_config WHERE level = ? AND map_id = ?',
                                 (self.level, self.map_id))
        raw_tiers = CONFIG_DB_CURSOR.fetchall()
        tiers_parsed = []
        for i in raw_tiers:
            tiers_parsed.append(i[0])

        for tier in tiers_parsed:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = True
            self.on_check_environment_unlock_conditions(tier)
            self.view.on_update_construction_state(ENVIRONMENT, tier)

    def on_put_under_construction(self, construction_type, entity_number):
        self.construction_state_matrix[construction_type][entity_number][UNLOCK_AVAILABLE] = False
        self.construction_state_matrix[construction_type][entity_number][UNDER_CONSTRUCTION] = True
        self.construction_state_matrix[construction_type][entity_number][CONSTRUCTION_TIME] \
            = self.construction_state_matrix[construction_type][entity_number][MAX_CONSTRUCTION_TIME]
        self.view.on_update_construction_state(construction_type, entity_number)
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.construction_state_matrix[construction_type][entity_number][PRICE])

    def on_add_money(self, money):
        self.money += money
        self.view.on_update_money(self.money)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money)

    def on_check_track_unlock_conditions(self, track):
        if self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_AVAILABLE] = True
            self.view.on_send_track_unlocked_notification(track)

    def on_check_environment_unlock_conditions(self, tier):
        if self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] \
                and self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_AVAILABLE] = True
            self.view.on_send_environment_unlocked_notification(tier)

    def on_activate_money_target(self, construction_type, row):
        self.money_target_activated = True
        self.money_target_cell_position = [construction_type, row]
        self.view.on_activate_money_target(construction_type, row)

    def on_deactivate_money_target(self):
        self.money_target_activated = False
        self.view.on_deactivate_money_target()
