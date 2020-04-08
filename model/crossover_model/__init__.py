from abc import ABC
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, TRUE, FALSE
from model import MapBaseModel


class CrossoverModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, track_param_1, track_param_2, crossover_type):
        super().__init__(
            controller, view, map_id, logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.model'
            )
        )
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.crossover_type = crossover_type
        self.busy = {track_param_1: {}, track_param_2: {}}
        self.force_busy = {track_param_1: {}, track_param_2: {}}
        self.last_entered_by = {track_param_1: {}, track_param_2: {}}
        self.state_change_listeners = {track_param_1: {}, track_param_2: {}}
        USER_DB_CURSOR.execute(
            '''SELECT busy_1_1, busy_1_2, busy_2_1, busy_2_2, force_busy_1_1, force_busy_1_2, 
            force_busy_2_1, force_busy_2_2 FROM crossovers 
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (self.track_param_1, self.track_param_2, self.crossover_type, self.map_id)
        )
        self.busy[self.track_param_1][self.track_param_1], self.busy[self.track_param_1][self.track_param_2], \
            self.busy[self.track_param_2][self.track_param_1], self.busy[self.track_param_2][self.track_param_2], \
            self.force_busy[self.track_param_1][self.track_param_1], \
            self.force_busy[self.track_param_1][self.track_param_2], \
            self.force_busy[self.track_param_2][self.track_param_1], \
            self.force_busy[self.track_param_2][self.track_param_2] = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute(
            '''SELECT last_entered_by_1_1, last_entered_by_1_2, last_entered_by_2_1, last_entered_by_2_2, 
            current_position_1, current_position_2 FROM crossovers 
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (self.track_param_1, self.track_param_2, self.crossover_type, self.map_id)
        )
        self.last_entered_by[self.track_param_1][self.track_param_1], \
            self.last_entered_by[self.track_param_1][self.track_param_2], \
            self.last_entered_by[self.track_param_2][self.track_param_1], \
            self.last_entered_by[self.track_param_2][self.track_param_2], \
            self.current_position_1, self.current_position_2 = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route, section_number FROM train_route_sections
            WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
            AND position_1 = ? AND position_2 = ? AND map_id = ?''',
            (
                self.track_param_1, self.track_param_2, self.crossover_type,
                self.track_param_1, self.track_param_1, self.map_id
            )
        )
        self.state_change_listeners[self.track_param_1][self.track_param_1] = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route, section_number FROM train_route_sections
            WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
            AND position_1 = ? AND position_2 = ? AND map_id = ?''',
            (
                self.track_param_1, self.track_param_2, self.crossover_type,
                self.track_param_1, self.track_param_2, self.map_id
            )
        )
        self.state_change_listeners[self.track_param_1][self.track_param_2] = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route, section_number FROM train_route_sections
            WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
            AND position_1 = ? AND position_2 = ? AND map_id = ?''',
            (
                self.track_param_1, self.track_param_2, self.crossover_type,
                self.track_param_2, self.track_param_1, self.map_id
            )
        )
        self.state_change_listeners[self.track_param_2][self.track_param_1] = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route, section_number FROM train_route_sections
            WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
            AND position_1 = ? AND position_2 = ? AND map_id = ?''',
            (
                self.track_param_1, self.track_param_2, self.crossover_type,
                self.track_param_2, self.track_param_2, self.map_id
            )
        )
        self.state_change_listeners[self.track_param_2][self.track_param_2] = CONFIG_DB_CURSOR.fetchall()
        USER_DB_CURSOR.execute(
            '''SELECT locked FROM crossovers 
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (self.track_param_1, self.track_param_2, self.crossover_type, self.map_id)
        )
        self.locked = USER_DB_CURSOR.fetchone()[0]

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute(
            '''UPDATE crossovers SET busy_1_1 = ?, busy_1_2 = ?, busy_2_1 = ?, busy_2_2 = ?, force_busy_1_1 = ?, 
            force_busy_1_2 = ?, force_busy_2_1 = ?, force_busy_2_2 = ?, last_entered_by_1_1 = ?, 
            last_entered_by_1_2 = ?, last_entered_by_2_1 = ?, last_entered_by_2_2 = ?, current_position_1 = ?, 
            current_position_2 = ?, locked = ?
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (
                self.busy[self.track_param_1][self.track_param_1], self.busy[self.track_param_1][self.track_param_2],
                self.busy[self.track_param_2][self.track_param_1], self.busy[self.track_param_2][self.track_param_2],
                self.force_busy[self.track_param_1][self.track_param_1],
                self.force_busy[self.track_param_1][self.track_param_2],
                self.force_busy[self.track_param_2][self.track_param_1],
                self.force_busy[self.track_param_2][self.track_param_2],
                self.last_entered_by[self.track_param_1][self.track_param_1],
                self.last_entered_by[self.track_param_1][self.track_param_2],
                self.last_entered_by[self.track_param_2][self.track_param_1],
                self.last_entered_by[self.track_param_2][self.track_param_2],
                self.current_position_1, self.current_position_2, self.locked,
                self.track_param_1, self.track_param_2, self.crossover_type, self.map_id
            )
        )

    @final
    def on_force_busy_on(self, positions, train_id):
        self.force_busy[positions[0]][positions[1]] = TRUE
        # if second position is not equal to first, no other train can fit inside,
        # so all 4 possible crossover routes are busy
        if positions[0] != positions[1]:
            self.on_busy_notify(positions[0], positions[0], train_id)
            self.on_busy_notify(positions[0], positions[1], train_id)
            self.on_busy_notify(positions[1], positions[0], train_id)
            self.on_busy_notify(positions[1], positions[1], train_id)
        # if second position is equal to first, there is some room for one more train,
        # so only 3 possible crossover routes are busy,
        # and route which second position is equal to first but both are not equal to initial one is not busy
        else:
            k = list(self.busy[positions[0]].keys())
            if positions[0] == k[0]:
                self.on_busy_notify(k[0], k[0], train_id)
                self.on_busy_notify(k[0], k[1], train_id)
                self.on_busy_notify(k[1], k[0], train_id)
            else:
                self.on_busy_notify(k[1], k[1], train_id)
                self.on_busy_notify(k[1], k[0], train_id)
                self.on_busy_notify(k[0], k[1], train_id)

        self.current_position_1, self.current_position_2 = positions
        self.view.on_change_current_position(self.current_position_1, self.current_position_2)

    @final
    def on_force_busy_off(self, positions):
        self.force_busy[positions[0]][positions[1]] = FALSE
        # if second position is not equal to first, no other train can fit inside,
        # so all 4 possible crossover routes are not busy now
        if positions[0] != positions[1]:
            self.on_leave_notify(positions[0], positions[0])
            self.on_leave_notify(positions[0], positions[1])
            self.on_leave_notify(positions[1], positions[0])
            self.on_leave_notify(positions[1], positions[1])
        # if second position is equal to first, there is some room for one more train,
        # so we need to check if this position is locked or not,
        # and if so, we do not unlock position locked by another train
        else:
            k = list(self.busy[positions[0]].keys())
            if positions[0] == k[0]:
                self.on_leave_notify(k[0], k[0])
                if not self.force_busy[k[1]][k[1]]:
                    self.on_leave_notify(k[0], k[1])
                    self.on_leave_notify(k[1], k[0])
            else:
                self.on_leave_notify(k[1], k[1])
                if not self.force_busy[k[0]][k[0]]:
                    self.on_leave_notify(k[1], k[0])
                    self.on_leave_notify(k[0], k[1])

    @final
    def on_busy_notify(self, position_1, position_2, train_id):
        self.busy[position_1][position_2] = TRUE
        self.last_entered_by[position_1][position_2] = train_id
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=TRUE)

    @final
    def on_leave_notify(self, position_1, position_2):
        self.busy[position_1][position_2] = FALSE
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=FALSE)
