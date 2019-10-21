from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class TrainRouteModel(MapBaseModel):
    def __init__(self, map_id, track, train_route):
        def sgn(x):
            if type(x) is not int:
                raise ValueError
            elif x == 0:
                return 0
            elif x > 0:
                return 1
            else:
                return -1

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.model'))
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT opened, last_opened_by, current_checkpoint, priority, cars 
                                  FROM train_routes WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (track, train_route, self.map_id))
        self.opened, self.last_opened_by, self.current_checkpoint, self.priority, self.cars \
            = USER_DB_CURSOR.fetchone()
        self.opened = bool(self.opened)
        USER_DB_CURSOR.execute('''SELECT train_route_section_busy_state FROM train_routes
                                  WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (track, train_route, self.map_id))
        self.train_route_section_busy_state \
            = list(map(bool, list(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))))
        CONFIG_DB_CURSOR.execute('''SELECT signal_track, signal_base_route FROM train_route_config
                                    WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (track, train_route, self.map_id))
        self.signal_track, self.signal_base_route = CONFIG_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT start_point_v2, stop_point_v2, destination_point_v2, checkpoints_v2 
                                    FROM train_route_config WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (track, train_route, self.map_id))
        fetched_data = list(CONFIG_DB_CURSOR.fetchone())
        for i in range(len(fetched_data)):
            if fetched_data[i] is not None:
                fetched_data[i] = tuple(map(int, fetched_data[i].split(',')))

        self.start_point_v2, self.stop_point_v2, self.destination_point_v2, self.checkpoints_v2 = fetched_data
        # trail points are stores in 3 parts:
        # first part is straight and is defined by start point and end point (always not null),
        # second part is defined by list of trail points (can be null),
        # third part is straight too and is defined by start point and end point (can be null)
        self.trail_points_v2_head_tail = []
        self.trail_points_v2_mid = []
        CONFIG_DB_CURSOR.execute('''SELECT trail_points_v2_part_1_start, trail_points_v2_part_1_end, 
                                    trail_points_v2_part_2_head_tail, trail_points_v2_part_2_mid, 
                                    trail_points_v2_part_3_start, trail_points_v2_part_3_end FROM train_route_config 
                                    WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (track, train_route, self.map_id))
        trail_points_v2_part_1_start, trail_points_v2_part_1_end, trail_points_v2_part_2_head_tail, \
            trail_points_v2_part_2_mid, trail_points_v2_part_3_start, trail_points_v2_part_3_end \
            = CONFIG_DB_CURSOR.fetchone()
        # parse start and end points for first part, append all points in between
        trail_points_v2_part_1_start_parsed = list(map(float, trail_points_v2_part_1_start.split(',')))
        trail_points_v2_part_1_end_parsed = list(map(float, trail_points_v2_part_1_end.split(',')))
        for i in range(round(trail_points_v2_part_1_start_parsed[0]), round(trail_points_v2_part_1_end_parsed[0]),
                       sgn(round(trail_points_v2_part_1_end_parsed[0] - trail_points_v2_part_1_start_parsed[0]))):
            self.trail_points_v2_head_tail.append((float(i), trail_points_v2_part_1_start_parsed[1],
                                                   trail_points_v2_part_1_start_parsed[2]))
            self.trail_points_v2_mid.append((float(i), trail_points_v2_part_1_start_parsed[1],
                                             trail_points_v2_part_1_start_parsed[2]))

        # parse second part, append all points
        if trail_points_v2_part_2_head_tail is not None:
            trail_points_v2_part_2_parsed = trail_points_v2_part_2_head_tail.split('|')
            for i in range(len(trail_points_v2_part_2_parsed)):
                trail_points_v2_part_2_parsed[i] = list(map(float, trail_points_v2_part_2_parsed[i].split(',')))

            self.trail_points_v2_head_tail.extend(trail_points_v2_part_2_parsed)

        if trail_points_v2_part_2_mid is not None:
            trail_points_v2_part_2_parsed = trail_points_v2_part_2_mid.split('|')
            for i in range(len(trail_points_v2_part_2_parsed)):
                trail_points_v2_part_2_parsed[i] = list(map(float, trail_points_v2_part_2_parsed[i].split(',')))

            self.trail_points_v2_mid.extend(trail_points_v2_part_2_parsed)

        # parse start and end points for third part, append all points in between
        if trail_points_v2_part_3_start is not None and trail_points_v2_part_3_end is not None:
            trail_points_v2_part_3_start_parsed = list(map(float, trail_points_v2_part_3_start.split(',')))
            trail_points_v2_part_3_end_parsed = list(map(float, trail_points_v2_part_3_end.split(',')))
            for i in range(round(trail_points_v2_part_3_start_parsed[0]), round(trail_points_v2_part_3_end_parsed[0]),
                           sgn(round(trail_points_v2_part_3_end_parsed[0] - trail_points_v2_part_3_start_parsed[0]))):
                self.trail_points_v2_head_tail.append((float(i), trail_points_v2_part_3_start_parsed[1],
                                                       trail_points_v2_part_3_start_parsed[2]))
                self.trail_points_v2_mid.append((float(i), trail_points_v2_part_3_start_parsed[1],
                                                 trail_points_v2_part_3_start_parsed[2]))

        CONFIG_DB_CURSOR.execute('''SELECT section_type, track_param_1, track_param_2 
                                    FROM train_route_sections WHERE track = ? and train_route = ? AND map_id = ?''',
                                 (track, train_route, self.map_id))
        self.train_route_sections = CONFIG_DB_CURSOR.fetchall()
        CONFIG_DB_CURSOR.execute('''SELECT position_1, position_2 
                                    FROM train_route_sections WHERE track = ? and train_route = ? AND map_id = ?''',
                                 (track, train_route, self.map_id))
        self.train_route_section_positions = CONFIG_DB_CURSOR.fetchall()

    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE train_routes SET opened = ?, last_opened_by = ?, current_checkpoint = ?,
                                  priority = ?, cars = ? WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (int(self.opened), self.last_opened_by, self.current_checkpoint, self.priority,
                                self.cars, self.controller.track, self.controller.train_route, self.map_id))
        busy_state_string = ','.join(list(map(str, list(map(int, self.train_route_section_busy_state)))))
        USER_DB_CURSOR.execute('''UPDATE train_routes SET train_route_section_busy_state = ? 
                                  WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (busy_state_string, self.controller.track, self.controller.train_route, self.map_id))

    def on_open_train_route(self, train_id, cars):
        self.opened = True
        self.last_opened_by = train_id
        self.cars = cars
        self.current_checkpoint = 0
        self.controller.parent_controller.on_set_trail_points(train_id, self.trail_points_v2_head_tail,
                                                              self.trail_points_v2_mid)
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

    @train_has_passed_train_route_section
    def on_update_train_route_sections(self, last_car_position):
        self.controller.parent_controller.on_train_route_section_force_busy_off(
            self.train_route_sections[self.current_checkpoint],
            self.train_route_section_positions[self.current_checkpoint])
        self.train_route_section_busy_state[self.current_checkpoint] = False
        if self.current_checkpoint == 0:
            self.controller.parent_controller.on_switch_signal_to_red(self.signal_track, self.signal_base_route)
            # for entry train route, section 0 is base entry, notify Map controller about entry state update
            if self.train_route_sections[0][0] in ENTRY_BASE_ROUTE[self.map_id]:
                self.controller.parent_controller\
                    .on_leave_entry(ENTRY_BASE_ROUTE[self.map_id].index(self.train_route_sections[0][0]))
            # for exit train route, section 0 is the track itself, notify Map controller about track state update
            elif self.train_route_sections[0][0] in ('left_exit_platform_base_route', 'right_exit_platform_base_route'):
                self.controller.parent_controller.on_leave_track(self.controller.track)

        # moving to the next section
        self.current_checkpoint += 1

    @train_route_is_opened
    @not_approaching_route
    def on_update_time(self):
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
