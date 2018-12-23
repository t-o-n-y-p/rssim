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


def _train_has_passed_train_route_section(fn):
    def _allow_other_trains_to_pass_if_train_has_passed_train_route_section(*args, **kwargs):
        if args[1] >= args[0].checkpoints_v2[args[0].current_checkpoint]:
            fn(*args, **kwargs)

    return _allow_other_trains_to_pass_if_train_has_passed_train_route_section


class TrainRouteModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.opened = None
        self.last_opened_by = None
        self.current_checkpoint = None
        self.start_point_v2 = None
        self.stop_point_v2 = None
        self.destination_point_v2 = None
        self.checkpoints_v2 = None
        self.trail_points_v2 = None
        self.signal_track = None
        self.signal_base_route = None
        self.train_route_sections = None
        self.train_route_section_positions = None
        self.train_route_section_busy_state = None
        self.train_id = None
        self.priority = None

    def on_train_route_setup(self, track, train_route):
        self.user_db_cursor.execute('''SELECT opened, last_opened_by, current_checkpoint FROM train_routes
                                       WHERE track = ? and train_route = ?''', (track, train_route))
        self.opened, self.last_opened_by, self.current_checkpoint = self.user_db_cursor.fetchone()
        self.opened = bool(self.opened)
        self.config_db_cursor.execute('''SELECT signal_track, signal_base_route FROM train_route_config
                                         WHERE track = ? and train_route = ?''', (track, train_route))
        self.signal_track, self.signal_base_route = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT start_point_v2, stop_point_v2, destination_point_v2, checkpoints_v2 
                                         FROM train_route_config WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        fetched_data = self.config_db_cursor.fetchone()
        for i in range(len(fetched_data)):
            if fetched_data[i] is not None:
                fetched_data[i] = fetched_data[i].split(',')
                for j in range(len(fetched_data[i])):
                    fetched_data[i][j] = int(fetched_data[i][j])

                fetched_data[i] = tuple(fetched_data[i])

        self.start_point_v2, self.stop_point_v2, self.destination_point_v2, self.checkpoints_v2 = fetched_data
        self.config_db_cursor.execute('''SELECT trail_points_v2 FROM train_route_config 
                                         WHERE track = ? and train_route = ?''', (track, train_route))
        trail_points_v2_parsed = self.config_db_cursor.fetchone()[0].split('|')
        for i in range(len(trail_points_v2_parsed)):
            trail_points_v2_parsed[i] = trail_points_v2_parsed[i].split(',')
            trail_points_v2_parsed[i][0] = int(trail_points_v2_parsed[i][0])
            trail_points_v2_parsed[i][1] = int(trail_points_v2_parsed[i][1])
            trail_points_v2_parsed[i][2] = float(trail_points_v2_parsed[i][2])

        self.config_db_cursor.execute('''SELECT section_type, track_param_1, track_param_2 
                                         FROM train_route_sections WHERE WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_sections = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT position_1, position_2 
                                         FROM train_route_sections WHERE WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_section_positions = self.config_db_cursor.fetchall()

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
        self.user_db_cursor.execute('''UPDATE train_routes SET opened = ?, last_opened_by = ?, current_checkpoint = ?
                                       WHERE track = ? and train_route = ?''',
                                    (int(self.opened), self.last_opened_by, self.current_checkpoint,
                                     self.controller.track, self.controller.train_route))

    def on_open_train_route(self, train_id):
        self.opened = True
        self.train_id = train_id
        self.last_opened_by = train_id
        self.current_checkpoint = 0
        self.controller.on_train_route_section_force_busy_on(self.train_route_sections[0],
                                                             self.train_route_section_positions[0], train_id)
        self.train_route_section_busy_state[0] = True

    def on_close_train_route(self):
        self.opened = False
        self.current_checkpoint = 0
        self.controller.on_train_route_section_force_busy_off(self.train_route_sections[-1],
                                                              self.train_route_section_positions[-1])
        self.train_route_section_busy_state[-1] = False

    @_train_has_passed_train_route_section
    def on_update_train_route_sections(self, last_car_position):
        self.controller.on_train_route_section_force_busy_off(
            self.train_route_sections[self.current_checkpoint],
            self.train_route_section_positions[self.current_checkpoint])
        self.train_route_section_busy_state[self.current_checkpoint] = False
        self.current_checkpoint += 1

    def on_update_time(self, game_time):
        train_route_busy = False
        for i in range(1, len(self.train_route_sections)):
            train_route_busy = train_route_busy or self.train_route_section_busy_state[i]

        if self.train_route_section_busy_state[0] and not train_route_busy:
            for i in range(1, len(self.train_route_sections)):
                self.controller.on_train_route_section_force_busy_on(
                    self.train_route_sections[i],
                    self.train_route_section_positions[i],
                    self.train_id)
                self.train_route_section_busy_state[i] = True

    def on_update_priority(self, priority):
        self.priority = priority
