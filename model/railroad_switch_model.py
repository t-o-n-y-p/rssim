from model import *


class RailroadSwitchModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.busy = None
        self.force_busy = None
        self.last_entered_by = None
        self.current_position = None
        self.state_change_listeners = []

    def on_railroad_switch_setup(self, track_param_1, track_param_2, switch_type):
        self.user_db_cursor.execute('''SELECT busy, force_busy, last_entered_by, current_position FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (track_param_1, track_param_2, switch_type))
        self.busy, self.force_busy, self.last_entered_by, self.current_position = self.user_db_cursor.fetchone()
        self.busy = bool(self.force_busy)
        self.force_busy = bool(self.force_busy)
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?''',
                                      (track_param_1, track_param_2, switch_type))
        self.state_change_listeners = self.config_db_cursor.fetchall()

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        self.user_db_cursor.execute('''UPDATE switches SET busy = ?, force_busy = ?, 
                                       last_entered_by = ?, current_position = ? 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (int(self.busy), int(self.force_busy), self.last_entered_by, self.current_position,
                                     self.controller.track_param_1, self.controller.track_param_2,
                                     self.controller.switch_type))

    def on_force_busy_on(self, positions, train_id):
        self.force_busy = True
        self.busy = True
        self.last_entered_by = train_id
        self.current_position = positions[0]
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

    def on_force_busy_off(self):
        self.force_busy = False
        self.busy = False
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)

