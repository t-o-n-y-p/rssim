from abc import ABC
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, CONSTRUCTION_STATE_MATRIX, TRACKS, ENVIRONMENT, LOCKED, \
    UNDER_CONSTRUCTION, CONSTRUCTION_TIME, UNLOCK_CONDITION_FROM_LEVEL, UNLOCK_CONDITION_FROM_PREVIOUS_TRACK, \
    UNLOCK_CONDITION_FROM_ENVIRONMENT, UNLOCK_AVAILABLE, UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT, \
    ENVIRONMENT_REQUIRED, TRUE, FALSE, MAX_CONSTRUCTION_TIME, PRICE
from model import MapBaseModel, MAXIMUM_ENVIRONMENT_TIER, MAXIMUM_TRACK_NUMBER


class ConstructorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.constructor.model'))
        self.cached_unlocked_tracks = []
        self.cached_unlocked_tiers = []
        USER_DB_CURSOR.execute('SELECT money_target_activated FROM constructor WHERE map_id = ?', (self.map_id, ))
        self.money_target_activated = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT money_target_cell_position FROM constructor WHERE map_id = ?', (self.map_id, ))
        self.money_target_cell_position = list(int(p) for p in USER_DB_CURSOR.fetchone()[0].split(','))

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute(
            '''UPDATE constructor SET money_target_activated = ?, money_target_cell_position = ? WHERE map_id = ?''',
            (
                self.money_target_activated,
                ','.join(str(p) for p in self.money_target_cell_position), self.map_id
            )
        )
        # if some tracks were unlocked since last time the game progress was saved,
        # they are not listed in track state matrix anymore, so their state is updated separately
        for track in self.cached_unlocked_tracks:
            USER_DB_CURSOR.execute(
                '''UPDATE tracks SET locked = 0, under_construction = 0, construction_time = 0, 
                unlock_condition_from_level = 0, unlock_condition_from_previous_track = 0, 
                unlock_condition_from_environment = 0, unlock_available = 0 WHERE track_number = ? AND map_id = ?''',
                (track, self.map_id)
            )

        self.cached_unlocked_tracks = []
        # locked tracks state is saved from track_state_matrix the same way it was read
        for track in CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS]:
            USER_DB_CURSOR.execute(
                '''UPDATE tracks SET locked = ?, under_construction = ?, construction_time = ?, 
                unlock_condition_from_level = ?, unlock_condition_from_previous_track = ?, 
                unlock_condition_from_environment = ?, unlock_available = ? WHERE track_number = ? AND map_id = ?''',
                (
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][LOCKED],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNDER_CONSTRUCTION],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][CONSTRUCTION_TIME],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_AVAILABLE], track, self.map_id
                )
            )

        # same for environment
        for tier in self.cached_unlocked_tiers:
            USER_DB_CURSOR.execute(
                '''UPDATE environment SET locked = 0, under_construction = 0, construction_time = 0, 
                unlock_condition_from_level = 0, unlock_condition_from_previous_environment = 0, unlock_available = 0 
                WHERE tier = ? AND map_id = ?''', (tier, self.map_id)
            )

        self.cached_unlocked_tiers = []
        for tier in CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT]:
            USER_DB_CURSOR.execute(
                '''UPDATE environment SET locked = ?, under_construction = ?, construction_time = ?, 
                unlock_condition_from_level = ?, unlock_condition_from_previous_environment = ?, unlock_available = ? 
                WHERE tier = ? AND map_id = ?''',
                (
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][LOCKED],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNDER_CONSTRUCTION],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][CONSTRUCTION_TIME],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][
                        UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT
                    ],
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_AVAILABLE], tier, self.map_id
                )
            )

    @final
    def on_update_time(self, dt):
        # unlocked_track stores track number if some track was unlocked and 0 otherwise
        unlocked_track = 0
        for track in CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS]:
            if CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNDER_CONSTRUCTION]:
                CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][CONSTRUCTION_TIME] \
                    += dt * self.dt_multiplier * self.construction_speed_bonus_multiplier
                if CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][CONSTRUCTION_TIME] \
                        >= CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][MAX_CONSTRUCTION_TIME]:
                    unlocked_track = track
                    self.controller.parent_controller.on_unlock_track(track)
                else:
                    self.view.on_update_construction_state(TRACKS, track)

        if unlocked_track > 0:
            self.on_remove_track_from_matrix(unlocked_track)

        # same for environment
        unlocked_tier = 0
        for tier in CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT]:
            if CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNDER_CONSTRUCTION]:
                CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][CONSTRUCTION_TIME] \
                    += dt * self.dt_multiplier * self.construction_speed_bonus_multiplier
                if CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][CONSTRUCTION_TIME] \
                        >= CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][MAX_CONSTRUCTION_TIME]:
                    unlocked_tier = tier
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNDER_CONSTRUCTION] = FALSE
                    CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][LOCKED] = FALSE
                    self.view.on_send_environment_construction_completed_notification(tier)
                    self.controller.parent_controller.on_unlock_environment(tier)
                    # tier is added to cached_unlocked_tracks list to be then correctly saved in the database
                    self.cached_unlocked_tiers.append(tier)
                    # unlock condition from environment is made up
                    for track in CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS]:
                        if CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][ENVIRONMENT_REQUIRED] == tier:
                            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                                = TRUE
                            self.on_check_track_unlock_conditions(track)
                            self.view.on_update_construction_state(TRACKS, track)

                    # if there are more tiers to unlock, unlock condition for the next tier is met
                    if tier < MAXIMUM_ENVIRONMENT_TIER[self.map_id]:
                        CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier + 1][
                            UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT
                        ] = TRUE
                        # if all 2 conditions are met for the next tier, it becomes available for construction
                        self.on_check_environment_unlock_conditions(tier + 1)

                    self.view.on_unlock_construction(ENVIRONMENT, tier)
                else:
                    self.view.on_update_construction_state(ENVIRONMENT, tier)

        if unlocked_tier > 0:
            CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT].pop(unlocked_tier)
            # if money target is activated for another tier, cell position is updated
            if self.money_target_activated and self.money_target_cell_position[0] == ENVIRONMENT \
                    and self.money_target_cell_position[1] > 0:
                self.money_target_cell_position[1] -= 1

        super().on_update_time(dt)

    @final
    def on_level_up(self):
        super().on_level_up()
        # determines if some tracks require level which was just hit
        CONFIG_DB_CURSOR.execute(
            'SELECT track_number FROM track_config WHERE level = ? AND map_id = ?', (self.level, self.map_id)
        )
        tracks_parsed = [t[0] for t in CONFIG_DB_CURSOR.fetchall()]
        # adjusts "unlock_from_level" condition for all tracks
        for track in tracks_parsed:
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = TRUE
            # if all three conditions are met, track is available for construction
            self.on_check_track_unlock_conditions(track)
            self.view.on_update_construction_state(TRACKS, track)

        # same for environment
        CONFIG_DB_CURSOR.execute(
            'SELECT tier FROM environment_config WHERE level = ? AND map_id = ?', (self.level, self.map_id)
        )
        tiers_parsed = [t[0] for t in CONFIG_DB_CURSOR.fetchall()]
        for tier in tiers_parsed:
            CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = TRUE
            self.on_check_environment_unlock_conditions(tier)
            self.view.on_update_construction_state(ENVIRONMENT, tier)

    @final
    def on_put_under_construction(self, construction_type, entity_number):
        CONSTRUCTION_STATE_MATRIX[self.map_id][construction_type][entity_number][UNLOCK_AVAILABLE] = FALSE
        CONSTRUCTION_STATE_MATRIX[self.map_id][construction_type][entity_number][UNDER_CONSTRUCTION] = TRUE
        self.view.on_update_construction_state(construction_type, entity_number)
        self.controller.parent_controller.parent_controller.on_pay_money(
            CONSTRUCTION_STATE_MATRIX[self.map_id][construction_type][entity_number][PRICE]
        )

    @final
    def on_check_track_unlock_conditions(self, track):
        if CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] \
                and CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] \
                and CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL]:
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_LEVEL] = FALSE
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = FALSE
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_CONDITION_FROM_ENVIRONMENT] = FALSE
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNLOCK_AVAILABLE] = TRUE
            self.view.on_send_track_unlocked_notification(track)

    @final
    def on_check_environment_unlock_conditions(self, tier):
        if CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] \
                and CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL]:
            CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT] \
                = FALSE
            CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_CONDITION_FROM_LEVEL] = FALSE
            CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][tier][UNLOCK_AVAILABLE] = TRUE
            self.view.on_send_environment_unlocked_notification(tier)

    @final
    def on_activate_money_target(self, construction_type, row):
        self.money_target_activated = TRUE
        self.money_target_cell_position = [construction_type, row]
        self.view.on_activate_money_target(construction_type, row)

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = FALSE
        self.view.on_deactivate_money_target()

    @final
    def on_unlock_track(self, track):
        CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][UNDER_CONSTRUCTION] = FALSE
        CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track][LOCKED] = FALSE
        self.view.on_send_track_construction_completed_notification(track)
        # track is added to cached_unlocked_tracks list to be then correctly saved in the database
        self.cached_unlocked_tracks.append(track)
        # if there are more tracks to unlock, unlock condition for the next track is met
        if track < MAXIMUM_TRACK_NUMBER[self.map_id]:
            CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][track + 1][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK] = TRUE
            # if all three conditions are met for the next track, it becomes available for construction
            self.on_check_track_unlock_conditions(track + 1)

        self.view.on_unlock_construction(TRACKS, track)

    @final
    def on_remove_track_from_matrix(self, unlocked_track):
        CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS].pop(unlocked_track)
        # if money target is activated for another track, cell position is updated
        if self.money_target_activated and self.money_target_cell_position[0] == TRACKS \
                and self.money_target_cell_position[1] > 0:
            self.money_target_cell_position[1] -= 1
