from logging import getLogger

from model import *


class CrossoverModel(Model):
    """
    Implements Crossover model.
    Crossover object is responsible for properties, UI and events related to the crossover.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor,
                 track_param_1, track_param_2, crossover_type):
        """
        Properties:
            busy                                indicates which crossover direction is busy
            force_busy                          indicates which crossover direction is force_busy
            last_entered_by                     train ID which made the crossover direction force_busy last time
            state_change_listeners              train route sections which share this crossover
            current_position_1                  current position crossover is switched to: track 1
            current_position_2                  current position crossover is switched to: track 2
            locked                              indicates if crossover is available for player

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track_param_1:                   number of the first track of two being connected by the crossover
        :param track_param_2:                   number of the second track of two being connected by the crossover
        :param crossover_type:                  crossover location: left/right side of the map
        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(
            user_db_connection, user_db_cursor, config_db_cursor,
            logger=getLogger(
                f'root.app.game.map.crossover.{track_param_1}.{track_param_2}.{crossover_type}.model'
            )
        )
        self.busy = {track_param_1: {}, track_param_2: {}}
        self.force_busy = {track_param_1: {}, track_param_2: {}}
        self.last_entered_by = {track_param_1: {}, track_param_2: {}}
        self.state_change_listeners = {track_param_1: {}, track_param_2: {}}
        self.user_db_cursor.execute('''SELECT busy_1_1, busy_1_2, busy_2_1, busy_2_2, force_busy_1_1, force_busy_1_2, 
                                       force_busy_2_1, force_busy_2_2 FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, crossover_type, self.map_id))
        self.busy[track_param_1][track_param_1], self.busy[track_param_1][track_param_2], \
            self.busy[track_param_2][track_param_1], self.busy[track_param_2][track_param_2], \
            self.force_busy[track_param_1][track_param_1], self.force_busy[track_param_1][track_param_2], \
            self.force_busy[track_param_2][track_param_1], self.force_busy[track_param_2][track_param_2] \
            = tuple(map(bool, self.user_db_cursor.fetchone()))
        self.user_db_cursor.execute('''SELECT last_entered_by_1_1, last_entered_by_1_2, 
                                       last_entered_by_2_1, last_entered_by_2_2, 
                                       current_position_1, current_position_2 FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, crossover_type, self.map_id))
        self.last_entered_by[track_param_1][track_param_1], self.last_entered_by[track_param_1][track_param_2], \
            self.last_entered_by[track_param_2][track_param_1], self.last_entered_by[track_param_2][track_param_2], \
            self.current_position_1, self.current_position_2 = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ? AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type,
                                       track_param_1, track_param_1, self.map_id))
        self.state_change_listeners[track_param_1][track_param_1] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ? AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type,
                                       track_param_1, track_param_2, self.map_id))
        self.state_change_listeners[track_param_1][track_param_2] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ? AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type,
                                       track_param_2, track_param_1, self.map_id))
        self.state_change_listeners[track_param_2][track_param_1] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ? AND map_id = ?''',
                                      (track_param_1, track_param_2, crossover_type,
                                       track_param_2, track_param_2, self.map_id))
        self.state_change_listeners[track_param_2][track_param_2] = self.config_db_cursor.fetchall()
        self.user_db_cursor.execute('''SELECT locked FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (track_param_1, track_param_2, crossover_type, self.map_id))
        self.locked = bool(self.user_db_cursor.fetchone()[0])

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        """
        Activates the Crossover view.
        """
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_save_state(self):
        """
        Saves crossover state to user progress database.
        """
        track_param_1 = self.controller.track_param_1
        track_param_2 = self.controller.track_param_2
        crossover_type = self.controller.crossover_type
        self.user_db_cursor.execute('''UPDATE crossovers SET busy_1_1 = ?, busy_1_2 = ?, busy_2_1 = ?, busy_2_2 = ?, 
                                       force_busy_1_1 = ?, force_busy_1_2 = ?, force_busy_2_1 = ?, force_busy_2_2 = ?, 
                                       last_entered_by_1_1 = ?, last_entered_by_1_2 = ?, last_entered_by_2_1 = ?, 
                                       last_entered_by_2_2 = ?, current_position_1 = ?, current_position_2 = ?,
                                       locked = ?
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                       AND map_id = ?''',
                                    (int(self.busy[track_param_1][track_param_1]),
                                     int(self.busy[track_param_1][track_param_2]),
                                     int(self.busy[track_param_2][track_param_1]),
                                     int(self.busy[track_param_2][track_param_2]),
                                     int(self.force_busy[track_param_1][track_param_1]),
                                     int(self.force_busy[track_param_1][track_param_2]),
                                     int(self.force_busy[track_param_2][track_param_1]),
                                     int(self.force_busy[track_param_2][track_param_2]),
                                     self.last_entered_by[track_param_1][track_param_1],
                                     self.last_entered_by[track_param_1][track_param_2],
                                     self.last_entered_by[track_param_2][track_param_1],
                                     self.last_entered_by[track_param_2][track_param_2],
                                     self.current_position_1, self.current_position_2, int(self.locked),
                                     track_param_1, track_param_2, crossover_type, self.map_id))

    def on_force_busy_on(self, positions, train_id):
        """
        Locks crossover in required position since the train is approaching.

        :param positions:               direction the train is about to proceed through
        :param train_id:                ID of the train which is about to pass through the crossover
        """
        self.force_busy[positions[0]][positions[1]] = True
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

    def on_force_busy_off(self, positions):
        """
        Unlocks crossover position after the train has passed it.

        :param positions:               direction that was previously locked for train
        """
        self.force_busy[positions[0]][positions[1]] = False
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

    def on_busy_notify(self, position_1, position_2, train_id):
        """
        Notifies all listeners about crossover positions state change.

        :param position_1:                      direction the train is about to proceed from
        :param position_2:                      direction the train is about to proceed to
        :param train_id:                        ID of the train which is about to pass through the crossover
        """
        self.busy[position_1][position_2] = True
        self.last_entered_by[position_1][position_2] = train_id
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

    def on_leave_notify(self, position_1, position_2):
        """
        Notifies all listeners about crossover positions state change.

        :param position_1:                      direction the train has proceed from
        :param position_2:                      direction the train has proceed to
        """
        self.busy[position_1][position_2] = False
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)

    def on_unlock(self):
        """
        Updates crossover lock state. Notifies the view about lock state update.
        """
        self.locked = False
        self.view.on_unlock()

    def on_update_map_id(self):
        self.map_id = 0
