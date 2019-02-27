from logging import getLogger

from model import *


class TrainRouteModel(Model):
    """
    Implements Train route model.
    Train route object is responsible for properties, UI and events related to the train route.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, track, train_route):
        """
        Properties:
            opened                              indicates if train route is opened
            last_opened_by                      train ID which opened train route last time
            current_checkpoint                  last force_busy train route section checkpoint
            priority                            train route priority
            cars                                number of cars for train which opened train route last time
            train_route_sections                switch and crossover matrix
            train_route_section_busy_state      indicates if switches and crossovers are busy
            train_route_section_positions       indicates correct switches and crossovers positions for thi train route
            signal_track                        number of track for the signal located on the train route
            signal_base_route                   base route code for the signal located on the train route
            start_point_v2                      list of start points for trains depending on number of cars
            stop_point_v2                       list of stop points for trains depending on number of cars
            destination_point_v2                list of destination points for trains depending on number of cars
            checkpoints_v2                      list of checkpoint numbers
            trail_points_v2                     list of train route points in 2D Cartesian coordinates
                                                plus rotation angle

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track:                           route track number
        :param train_route:                     route type (e.g. left/right entry/exit)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger(f'root.app.game.map.train_route.{track}.{train_route}.model'))
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

        self.trail_points_v2 = trail_points_v2_parsed
        self.config_db_cursor.execute('''SELECT section_type, track_param_1, track_param_2 
                                         FROM train_route_sections WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_sections = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT position_1, position_2 
                                         FROM train_route_sections WHERE track = ? and train_route = ?''',
                                      (track, train_route))
        self.train_route_section_positions = self.config_db_cursor.fetchall()

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        """
        Activates the view.
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
        Saves train route state to user progress database.
        """
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
        """
        Opens train route.

        :param train_id:                        ID of the train which opens the train route
        :param cars:                            number of cars in the train
        """
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
        """
        Closes train route.
        """
        self.opened = False
        self.current_checkpoint = 0
        self.train_route_section_busy_state[-1] = False
        self.cars = 0

    @train_has_passed_train_route_section
    def on_update_train_route_sections(self, last_car_position):
        """
        Updates train route section state based on last car position.

        :param last_car_position:               train last car position on the route
        """
        self.controller.parent_controller.on_train_route_section_force_busy_off(
            self.train_route_sections[self.current_checkpoint],
            self.train_route_section_positions[self.current_checkpoint])
        self.train_route_section_busy_state[self.current_checkpoint] = False
        if self.current_checkpoint == 0:
            self.controller.parent_controller.on_switch_signal_to_red(self.signal_track, self.signal_base_route)
            # for entry train route, section 0 is base entry, notify Map controller about entry state update
            if self.train_route_sections[0][0] == 'left_entry_base_route':
                self.controller.parent_controller.on_leave_entry(DIRECTION_FROM_LEFT_TO_RIGHT)
            elif self.train_route_sections[0][0] == 'right_entry_base_route':
                self.controller.parent_controller.on_leave_entry(DIRECTION_FROM_RIGHT_TO_LEFT)
            elif self.train_route_sections[0][0] == 'left_side_entry_base_route':
                self.controller.parent_controller.on_leave_entry(DIRECTION_FROM_LEFT_TO_RIGHT_SIDE)
            elif self.train_route_sections[0][0] == 'right_side_entry_base_route':
                self.controller.parent_controller.on_leave_entry(DIRECTION_FROM_RIGHT_TO_LEFT_SIDE)
            # for exit train route, section 0 is the track itself, notify Map controller about track state update
            elif self.train_route_sections[0][0] in ('left_exit_platform_base_route', 'right_exit_platform_base_route'):
                self.controller.parent_controller.on_leave_track(self.controller.track)

        # moving to the next section
        self.current_checkpoint += 1

    @train_route_is_opened
    @not_approaching_route
    def on_update_time(self, game_time):
        """
        Every frame this method checks if there is a train waiting at signal at danger
        and if all other sections are not busy. If so, updates signal state and lets train go.

        :param game_time:               current in-game time
        """
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
        """
        Updates train route priority value.

        :param priority:                        new priority value
        """
        self.priority = priority

    def on_update_section_status(self, section, status):
        """
        Updates train route section status.

        :param section:                         train route section number
        :param status:                          new status
        """
        self.train_route_section_busy_state[section] = status
