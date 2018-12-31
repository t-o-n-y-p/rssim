from .model_base import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class CrossoverModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.busy = {}
        self.force_busy = {}
        self.last_entered_by = {}
        self.current_position_1 = None
        self.current_position_2 = None
        self.state_change_listeners = {}

    def on_crossover_setup(self, track_param_1, track_param_2, crossover_type):
        self.busy[track_param_1] = {}
        self.busy[track_param_2] = {}
        self.force_busy[track_param_1] = {}
        self.force_busy[track_param_2] = {}
        self.last_entered_by[track_param_1] = {}
        self.last_entered_by[track_param_2] = {}
        self.state_change_listeners[track_param_1] = {}
        self.state_change_listeners[track_param_2] = {}
        self.user_db_cursor.execute('''SELECT busy_1_1, busy_1_2, busy_2_1, busy_2_2, force_busy_1_1, force_busy_1_2, 
                                       force_busy_2_1, force_busy_2_2, last_entered_by_1_1, last_entered_by_1_2, 
                                       last_entered_by_2_1, last_entered_by_2_2, current_position_1, current_position_2 
                                       FROM crossovers 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ?''',
                                    (track_param_1, track_param_2, crossover_type))
        self.busy[track_param_1][track_param_1], self.busy[track_param_1][track_param_2], \
            self.busy[track_param_2][track_param_1], self.busy[track_param_2][track_param_2], \
            self.force_busy[track_param_1][track_param_1], self.force_busy[track_param_1][track_param_2], \
            self.force_busy[track_param_2][track_param_1], self.force_busy[track_param_2][track_param_2], \
            self.last_entered_by[track_param_1][track_param_1], self.last_entered_by[track_param_1][track_param_2], \
            self.last_entered_by[track_param_2][track_param_1], self.last_entered_by[track_param_2][track_param_2], \
            self.current_position_1, self.current_position_2 = self.user_db_cursor.fetchone()
        self.busy[track_param_1][track_param_1] = bool(self.busy[track_param_1][track_param_1])
        self.busy[track_param_1][track_param_2] = bool(self.busy[track_param_1][track_param_2])
        self.busy[track_param_2][track_param_1] = bool(self.busy[track_param_2][track_param_1])
        self.busy[track_param_2][track_param_2] = bool(self.busy[track_param_2][track_param_2])
        self.force_busy[track_param_1][track_param_1] = bool(self.force_busy[track_param_1][track_param_1])
        self.force_busy[track_param_1][track_param_2] = bool(self.force_busy[track_param_1][track_param_2])
        self.force_busy[track_param_2][track_param_1] = bool(self.force_busy[track_param_2][track_param_1])
        self.force_busy[track_param_2][track_param_2] = bool(self.force_busy[track_param_2][track_param_2])
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ?''',
                                      (track_param_1, track_param_2, crossover_type, track_param_1, track_param_1))
        self.state_change_listeners[track_param_1][track_param_1] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ?''',
                                      (track_param_1, track_param_2, crossover_type, track_param_1, track_param_2))
        self.state_change_listeners[track_param_1][track_param_2] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ?''',
                                      (track_param_1, track_param_2, crossover_type, track_param_2, track_param_1))
        self.state_change_listeners[track_param_2][track_param_1] = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?
                                         AND position_1 = ? AND position_2 = ?''',
                                      (track_param_1, track_param_2, crossover_type, track_param_2, track_param_2))
        self.state_change_listeners[track_param_2][track_param_2] = self.config_db_cursor.fetchall()

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        track_param_1 = self.controller.track_param_1
        track_param_2 = self.controller.track_param_2
        crossover_type = self.controller.crossover_type
        self.user_db_cursor.execute('''UPDATE crossovers SET busy_1_1 = ?, busy_1_2 = ?, busy_2_1 = ?, busy_2_2 = ?, 
                                       force_busy_1_1 = ?, force_busy_1_2 = ?, force_busy_2_1 = ?, force_busy_2_2 = ?, 
                                       last_entered_by_1_1 = ?, last_entered_by_1_2 = ?, last_entered_by_2_1 = ?, 
                                       last_entered_by_2_2 = ?, current_position_1 = ?, current_position_2 = ?
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ?''',
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
                                     self.current_position_1, self.current_position_2,
                                     track_param_1, track_param_2, crossover_type))

    def on_force_busy_on(self, positions, train_id):
        self.force_busy[positions[0]][positions[1]] = True
        if positions[0] != positions[1]:
            self.on_busy_notify(positions[0], positions[0], train_id)
            self.on_busy_notify(positions[0], positions[1], train_id)
            self.on_busy_notify(positions[1], positions[0], train_id)
            self.on_busy_notify(positions[1], positions[1], train_id)
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
        self.force_busy[positions[0]][positions[1]] = False
        if positions[0] != positions[1]:
            self.on_leave_notify(positions[0], positions[0])
            self.on_leave_notify(positions[0], positions[1])
            self.on_leave_notify(positions[1], positions[0])
            self.on_leave_notify(positions[1], positions[1])
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
        self.busy[position_1][position_2] = True
        self.last_entered_by[position_1][position_2] = train_id
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

    def on_leave_notify(self, position_1, position_2):
        self.busy[position_1][position_2] = False
        for listener in self.state_change_listeners[position_1][position_2]:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)
