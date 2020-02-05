from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, CONSTRUCTION_STATE_MATRIX


class ConstructorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.constructor.model'))
        self.construction_state_matrix = CONSTRUCTION_STATE_MATRIX[self.map_id]
        self.cached_unlocked_tracks = []
        self.cached_unlocked_tiers = []
        USER_DB_CURSOR.execute('SELECT money_target_activated FROM constructor WHERE map_id = ?', (self.map_id, ))
        self.money_target_activated = bool(USER_DB_CURSOR.fetchone()[0])
        USER_DB_CURSOR.execute('SELECT money_target_cell_position FROM constructor WHERE map_id = ?', (self.map_id, ))
        self.money_target_cell_position = list(int(p) for p in USER_DB_CURSOR.fetchone()[0].split(','))

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE constructor SET money_target_activated = ?, money_target_cell_position = ? 
                                  WHERE map_id = ?''',
                               (int(self.money_target_activated),
                                ','.join(str(p) for p in self.money_target_cell_position), self.map_id))
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
                                       int(i) for i in (
                                           self.construction_state_matrix[TRACKS][track][LOCKED],
                                           self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION],
                                           self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME],
                                           self.construction_state_matrix[TRACKS][track][
                                                    UNLOCK_CONDITION_FROM_LEVEL],
                                           self.construction_state_matrix[TRACKS][track][
                                                    UNLOCK_CONDITION_FROM_PREVIOUS_TRACK],
                                           self.construction_state_matrix[TRACKS][track][
                                                    UNLOCK_CONDITION_FROM_ENVIRONMENT],
                                           self.construction_state_matrix[TRACKS][track][UNLOCK_AVAILABLE],
                                           track, self.map_id
                                       )
                                   ))

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
                                       int(i) for i in (
                                           self.construction_state_matrix[ENVIRONMENT][tier][LOCKED],
                                           self.construction_state_matrix[ENVIRONMENT][tier][UNDER_CONSTRUCTION],
                                           self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME],
                                           self.construction_state_matrix[ENVIRONMENT][tier][
                                                    UNLOCK_CONDITION_FROM_LEVEL],
                                           self.construction_state_matrix[ENVIRONMENT][tier][
                                                    UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT],
                                           self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_AVAILABLE],
                                           tier, self.map_id)
                                   ))

    @final
    def on_update_time(self):
        super().on_update_time()
        # unlocked_track stores track number if some track was unlocked and 0 otherwise
        unlocked_track = 0
        for track in self.construction_state_matrix[TRACKS]:
            if self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION]:
                self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME] -= 1
                if self.construction_state_matrix[TRACKS][track][CONSTRUCTION_TIME] <= 0:
                    unlocked_track = track
                    self.controller.parent_controller.on_unlock_track(track)
                else:
                    self.view.on_update_construction_state(TRACKS, track)

        if unlocked_track > 0:
            self.on_remove_track_from_matrix(unlocked_track)

        # same for environment
        unlocked_tier = 0
        for tier in self.construction_state_matrix[ENVIRONMENT]:
            if self.construction_state_matrix[ENVIRONMENT][tier][UNDER_CONSTRUCTION]:
                self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME] -= 1
                if self.construction_state_matrix[ENVIRONMENT][tier][CONSTRUCTION_TIME] <= 0:
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
                    self.view.on_update_construction_state(ENVIRONMENT, tier)

        if unlocked_tier > 0:
            self.construction_state_matrix[ENVIRONMENT].pop(unlocked_tier)
            # if money target is activated for another tier, cell position is updated
            if self.money_target_activated and self.money_target_cell_position[0] == ENVIRONMENT \
                    and self.money_target_cell_position[1] > 0:
                self.money_target_cell_position[1] -= 1

    @final
    def on_level_up(self):
        super().on_level_up()
        # determines if some tracks require level which was just hit
        CONFIG_DB_CURSOR.execute('SELECT track_number FROM track_config WHERE level = ? AND map_id = ?',
                                 (self.level, self.map_id))
        tracks_parsed = [t[0] for t in CONFIG_DB_CURSOR.fetchall()]
        # adjusts "unlock_from_level" condition for all tracks
        for track in tracks_parsed:
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = True
            # if all three conditions are met, track is available for construction
            self.on_check_track_unlock_conditions(track)
            self.view.on_update_construction_state(TRACKS, track)

        # same for environment
        CONFIG_DB_CURSOR.execute('SELECT tier FROM environment_config WHERE level = ? AND map_id = ?',
                                 (self.level, self.map_id))
        tiers_parsed = [t[0] for t in CONFIG_DB_CURSOR.fetchall()]
        for tier in tiers_parsed:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = True
            self.on_check_environment_unlock_conditions(tier)
            self.view.on_update_construction_state(ENVIRONMENT, tier)

    @final
    def on_put_under_construction(self, construction_type, entity_number):
        self.construction_state_matrix[construction_type][entity_number][UNLOCK_AVAILABLE] = False
        self.construction_state_matrix[construction_type][entity_number][UNDER_CONSTRUCTION] = True
        self.construction_state_matrix[construction_type][entity_number][CONSTRUCTION_TIME] \
            = int(self.construction_state_matrix[construction_type][entity_number][MAX_CONSTRUCTION_TIME]
                  * self.construction_time_bonus_multiplier)
        self.view.on_update_construction_state(construction_type, entity_number)
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.construction_state_matrix[construction_type][entity_number][PRICE])

    @final
    def on_check_track_unlock_conditions(self, track):
        if self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                and self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = False
            self.construction_state_matrix[TRACKS][track][UNLOCK_AVAILABLE] = True
            self.view.on_send_track_unlocked_notification(track)

    @final
    def on_check_environment_unlock_conditions(self, tier):
        if self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] \
                and self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL]:
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.construction_state_matrix[ENVIRONMENT][tier][UNLOCK_AVAILABLE] = True
            self.view.on_send_environment_unlocked_notification(tier)

    @final
    def on_activate_money_target(self, construction_type, row):
        self.money_target_activated = True
        self.money_target_cell_position = [construction_type, row]
        self.view.on_activate_money_target(construction_type, row)

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = False
        self.view.on_deactivate_money_target()

    @final
    def on_unlock_track(self, track):
        self.construction_state_matrix[TRACKS][track][UNDER_CONSTRUCTION] = False
        self.construction_state_matrix[TRACKS][track][LOCKED] = False
        self.view.on_send_track_construction_completed_notification(track)
        # track is added to cached_unlocked_tracks list to be then correctly saved in the database
        self.cached_unlocked_tracks.append(track)
        # if there are more tracks to unlock, unlock condition for the next track is met
        if track < MAXIMUM_TRACK_NUMBER[self.map_id]:
            self.construction_state_matrix[TRACKS][track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = True
            # if all three conditions are met for the next track, it becomes available for construction
            self.on_check_track_unlock_conditions(track + 1)

        self.view.on_unlock_construction(TRACKS, track)

    @final
    def on_remove_track_from_matrix(self, unlocked_track):
        self.construction_state_matrix[TRACKS].pop(unlocked_track)
        # if money target is activated for another track, cell position is updated
        if self.money_target_activated and self.money_target_cell_position[0] == TRACKS \
                and self.money_target_cell_position[1] > 0:
            self.money_target_cell_position[1] -= 1
