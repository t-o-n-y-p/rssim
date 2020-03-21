from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, TrailPointsV2


class TrainRouteModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, track, train_route):
        super().__init__(controller, view, map_id,
                         logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.model'))
        self.track = track
        self.train_route = train_route
        USER_DB_CURSOR.execute('''SELECT opened, last_opened_by, current_checkpoint, priority, cars 
                                  FROM train_routes WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (self.track, self.train_route, self.map_id))
        self.opened, self.last_opened_by, self.current_checkpoint, self.priority, self.cars = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT train_route_section_busy_state FROM train_routes
                                  WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (self.track, self.train_route, self.map_id))
        self.train_route_section_busy_state = [int(s) for s in USER_DB_CURSOR.fetchone()[0].split(',')]
        CONFIG_DB_CURSOR.execute('''SELECT start_point_v2, stop_point_v2, destination_point_v2, checkpoints_v2 
                                    FROM train_route_config WHERE track = ? AND train_route = ? AND map_id = ?''',
                                 (self.track, self.train_route, self.map_id))
        fetched_data = list(CONFIG_DB_CURSOR.fetchone())
        for i in range(len(fetched_data)):
            if fetched_data[i] is not None:
                fetched_data[i] = tuple(int(p) for p in fetched_data[i].split(','))

        self.start_point_v2, self.stop_point_v2, self.destination_point_v2, self.checkpoints_v2 = fetched_data
        self.trail_points_v2 = TrailPointsV2(self.map_id, self.track, self.train_route)
        CONFIG_DB_CURSOR.execute('''SELECT section_type, track_param_1, track_param_2 
                                    FROM train_route_sections WHERE track = ? and train_route = ? AND map_id = ?''',
                                 (self.track, self.train_route, self.map_id))
        self.train_route_sections = CONFIG_DB_CURSOR.fetchall()
        self.signal_base_route, self.signal_track = None, None
        if len(self.train_route_sections) > 1:
            self.signal_base_route, self.signal_track = self.train_route_sections[0][:2]

        CONFIG_DB_CURSOR.execute('''SELECT position_1, position_2 
                                    FROM train_route_sections WHERE track = ? and train_route = ? AND map_id = ?''',
                                 (self.track, self.train_route, self.map_id))
        self.train_route_section_positions = CONFIG_DB_CURSOR.fetchall()

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE train_routes SET opened = ?, last_opened_by = ?, current_checkpoint = ?,
                                  priority = ?, cars = ?, train_route_section_busy_state = ? 
                                  WHERE track = ? AND train_route = ? AND map_id = ?''',
                               (self.opened, self.last_opened_by, self.current_checkpoint, self.priority,
                                self.cars, ','.join(str(t) for t in self.train_route_section_busy_state),
                                self.track, self.train_route, self.map_id))

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        if self.opened and len(self.train_route_sections) > 1:
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
                    self.train_route_section_busy_state[i] = TRUE

                self.train_route_section_busy_state[-1] = TRUE

    @final
    def on_open_train_route(self, train_id, cars):
        self.opened = TRUE
        self.last_opened_by = train_id
        self.cars = cars
        self.current_checkpoint = 0
        self.controller.parent_controller.on_set_trail_points(train_id, self.trail_points_v2)
        self.controller.parent_controller.on_set_train_stop_point(train_id, self.stop_point_v2[cars])
        self.controller.parent_controller.on_set_train_destination_point(train_id, self.destination_point_v2[cars])
        if self.start_point_v2 is not None:
            self.controller.parent_controller.on_set_train_start_point(train_id, self.start_point_v2[cars])

        self.train_route_section_busy_state[0] = TRUE

    @final
    def on_close_train_route(self):
        self.opened = FALSE
        self.current_checkpoint = 0
        self.train_route_section_busy_state[-1] = FALSE
        self.cars = 0

    @final
    @train_has_passed_train_route_section
    def on_update_train_route_sections(self, last_car_position):
        self.controller.parent_controller.on_train_route_section_force_busy_off(
            self.train_route_sections[self.current_checkpoint],
            self.train_route_section_positions[self.current_checkpoint])
        self.train_route_section_busy_state[self.current_checkpoint] = FALSE
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

    @final
    def on_update_priority(self, priority):
        self.priority = priority

    @final
    def on_update_section_status(self, section, status):
        self.train_route_section_busy_state[section] = status
