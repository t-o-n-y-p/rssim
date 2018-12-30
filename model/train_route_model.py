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


def _train_route_is_opened(fn):
    def _handle_if_train_route_is_opened(*args, **kwargs):
        if args[0].opened:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_opened


class TrainRouteModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3
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
        self.priority = None
        self.cars = None

    def on_train_route_setup(self, track, train_route):
        self.user_db_cursor.execute('''SELECT opened, last_opened_by, current_checkpoint, priority, cars 
                                       FROM train_routes WHERE track = ? and train_route = ?''', (track, train_route))
        self.opened, self.last_opened_by, self.current_checkpoint, self.priority, self.cars \
            = self.user_db_cursor.fetchone()
        self.opened = bool(self.opened)
        self.user_db_cursor.execute('''SELECT train_route_section_busy_state FROM train_routes
                                       WHERE track = ? and train_route = ?''', (track, train_route))
        busy_state_parsed = self.user_db_cursor.fetchone()[0].split(',')
        for i in range(len(busy_state_parsed)):
            busy_state_parsed[i] = bool(int(busy_state_parsed[i]))

        self.train_route_section_busy_state = busy_state_parsed

        self.config_db_cursor.execute('''SELECT signal_track, signal_base_route FROM train_route_config
                                         WHERE track = ? and train_route = ?''', (track, train_route))
        self.signal_track, self.signal_base_route = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT start_point_v2, stop_point_v2, destination_point_v2, checkpoints_v2 
                                         FROM train_route_config WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        fetched_data = list(self.config_db_cursor.fetchone())
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
                                         FROM train_route_sections WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_sections = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT position_1, position_2 
                                         FROM train_route_sections WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_section_positions = self.config_db_cursor.fetchall()
        if self.opened:
            self.controller.parent_controller.on_set_trail_points(self.last_opened_by, self.trail_points_v2)

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
        self.user_db_cursor.execute('''UPDATE train_routes SET opened = ?, last_opened_by = ?, current_checkpoint = ?,
                                       priority = ?, cars = ? WHERE track = ? and train_route = ?''',
                                    (int(self.opened), self.last_opened_by, self.current_checkpoint, self.priority,
                                     self.cars, self.controller.track, self.controller.train_route))
        busy_state_string = ''
        for i in self.train_route_section_busy_state:
            busy_state_string += f'{int(i)},'

        busy_state_string = busy_state_string[0:len(busy_state_string) - 1]
        self.user_db_cursor.execute('''UPDATE train_routes SET train_route_section_busy_state = ? 
                                       WHERE track = ? and train_route = ?''',
                                    (busy_state_string, self.controller.track, self.controller.train_route))

    def on_open_train_route(self, train_id, cars):
        self.opened = True
        self.last_opened_by = train_id
        self.cars = cars
        self.current_checkpoint = 0
        self.controller.parent_controller.on_set_trail_points(train_id, self.trail_points_v2)
        if self.start_point_v2 is not None:
            self.controller.parent_controller.on_set_train_start_point(train_id, self.start_point_v2[cars])

        self.controller.parent_controller.on_set_train_stop_point(train_id, self.stop_point_v2[cars])
        self.controller.parent_controller.on_set_train_destination_point(train_id, self.destination_point_v2[cars])
        self.train_route_section_busy_state[0] = True

    def on_close_train_route(self):
        self.opened = False
        self.current_checkpoint = 0
        self.train_route_section_busy_state[-1] = False
        self.cars = 0

    @_train_has_passed_train_route_section
    def on_update_train_route_sections(self, last_car_position):
        self.controller.parent_controller.on_train_route_section_force_busy_off(
            self.train_route_sections[self.current_checkpoint],
            self.train_route_section_positions[self.current_checkpoint])
        self.train_route_section_busy_state[self.current_checkpoint] = False
        if self.current_checkpoint == 0:
            self.controller.parent_controller.on_switch_signal_to_red(self.signal_track, self.signal_base_route)
            if self.train_route_sections[0][0] == 'left_entry_base_route':
                self.controller.parent_controller.on_leave_entry(self.direction_from_left_to_right)
            elif self.train_route_sections[0][0] == 'right_entry_base_route':
                self.controller.parent_controller.on_leave_entry(self.direction_from_right_to_left)
            elif self.train_route_sections[0][0] == 'left_side_entry_base_route':
                self.controller.parent_controller.on_leave_entry(self.direction_from_left_to_right_side)
            elif self.train_route_sections[0][0] == 'right_side_entry_base_route':
                self.controller.parent_controller.on_leave_entry(self.direction_from_right_to_left_side)
            elif self.train_route_sections[0][0] in ('left_exit_platform_base_route', 'right_exit_platform_base_route'):
                self.controller.parent_controller.on_leave_track(self.controller.track)

        self.current_checkpoint += 1

    @_train_route_is_opened
    def on_update_time(self, game_time):
        train_route_busy = False
        for i in range(1, len(self.train_route_sections)):
            train_route_busy = train_route_busy or self.train_route_section_busy_state[i]

        if self.train_route_section_busy_state[0] and not train_route_busy:
            self.controller.parent_controller.on_switch_signal_to_green(self.signal_track, self.signal_base_route)
            self.controller.parent_controller.on_set_train_stop_point(self.last_opened_by,
                                                                      self.destination_point_v2[self.cars])
            for i in range(1, len(self.train_route_sections) - 1):
                self.controller.parent_controller.on_train_route_section_force_busy_on(
                    self.train_route_sections[i],
                    self.train_route_section_positions[i],
                    self.last_opened_by)
                self.train_route_section_busy_state[i] = True

            self.train_route_section_busy_state[-1] = True

    def on_update_priority(self, priority):
        self.priority = priority

    def on_update_section_status(self, section, status):
        self.train_route_section_busy_state[section] = status