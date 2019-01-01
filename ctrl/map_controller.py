from operator import attrgetter

from .controller_base import Controller


def _controller_is_active(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def _controller_is_not_active(fn):
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


def _map_view_is_active(fn):
    def _handle_if_map_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_map_view_is_activated


class MapController(Controller):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller)
        self.scheduler = None
        self.constructor = None
        self.dispatcher = None
        self.signals = {}
        self.signals_list = []
        self.train_routes = {}
        self.train_routes_sorted_list = []
        self.switches = {}
        self.switches_list = []
        self.crossovers = {}
        self.crossovers_list = []
        self.trains = {}

    def on_update_view(self):
        self.view.on_update()
        self.scheduler.on_update_view()
        self.dispatcher.on_update_view()
        for signal in self.signals_list:
            signal.on_update_view()

        for route in self.train_routes_sorted_list:
            route.on_update_view()

        for switch in self.switches_list:
            switch.on_update_view()

        for crossover in self.crossovers_list:
            crossover.on_update_view()

        for train_id in self.trains:
            self.trains[train_id].on_update_view()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.scheduler.on_activate()
        self.dispatcher.on_activate()
        for signal in self.signals_list:
            signal.on_activate()

        for route in self.train_routes_sorted_list:
            route.on_activate()

        for switch in self.switches_list:
            switch.on_activate()

        for crossover in self.crossovers_list:
            crossover.on_activate()

        for train_id in self.trains:
            self.trains[train_id].on_activate()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.scheduler.on_deactivate()
        self.dispatcher.on_deactivate()
        for signal in self.signals_list:
            signal.on_deactivate()

        for route in self.train_routes_sorted_list:
            route.on_deactivate()

        for switch in self.switches_list:
            switch.on_deactivate()

        for crossover in self.crossovers_list:
            crossover.on_deactivate()

        for train_id in self.trains:
            self.trains[train_id].on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.scheduler.on_change_screen_resolution(screen_resolution)
        self.dispatcher.on_change_screen_resolution(screen_resolution)
        for signal in self.signals_list:
            signal.on_change_screen_resolution(screen_resolution)

        for route in self.train_routes_sorted_list:
            route.on_change_screen_resolution(screen_resolution)

        for switch in self.switches_list:
            switch.on_change_screen_resolution(screen_resolution)

        for crossover in self.crossovers_list:
            crossover.on_change_screen_resolution(screen_resolution)

        for train_id in self.trains:
            self.trains[train_id].on_change_screen_resolution(screen_resolution)

        self.on_change_base_offset(self.view.base_offset)

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)
        for signal in self.signals_list:
            signal.on_change_base_offset(new_base_offset)

        for route in self.train_routes_sorted_list:
            route.on_change_base_offset(new_base_offset)

        for switch in self.switches_list:
            switch.on_change_base_offset(new_base_offset)

        for crossover in self.crossovers_list:
            crossover.on_change_base_offset(new_base_offset)

        for train_id in self.trains:
            self.trains[train_id].on_change_base_offset(new_base_offset)

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)
        self.scheduler.on_unlock_track(track_number)
        self.dispatcher.on_unlock_track(track_number)
        for i in self.signals[track_number]:
            self.signals[track_number][i].on_unlock()

    def on_activate_view(self):
        self.view.on_activate()
        for signal in self.signals_list:
            signal.on_activate_view()

        for route in self.train_routes_sorted_list:
            route.on_activate_view()

        for switch in self.switches_list:
            switch.on_activate_view()

        for crossover in self.crossovers_list:
            crossover.on_activate_view()

        for train_id in self.trains:
            self.trains[train_id].on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.scheduler.on_deactivate_view()
        for signal in self.signals_list:
            signal.on_deactivate_view()

        for route in self.train_routes_sorted_list:
            route.on_deactivate_view()

        for switch in self.switches_list:
            switch.on_deactivate_view()

        for crossover in self.crossovers_list:
            crossover.on_deactivate_view()

        for train_id in self.trains:
            self.trains[train_id].on_deactivate_view()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)
        for signal in self.signals_list:
            signal.on_zoom_in()

        for route in self.train_routes_sorted_list:
            route.on_zoom_in()

        for switch in self.switches_list:
            switch.on_zoom_in()

        for crossover in self.crossovers_list:
            crossover.on_zoom_in()

        for train_id in self.trains:
            self.trains[train_id].on_zoom_in()

        self.on_change_base_offset(self.view.base_offset)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)
        for signal in self.signals_list:
            signal.on_zoom_out()

        for route in self.train_routes_sorted_list:
            route.on_zoom_out()

        for switch in self.switches_list:
            switch.on_zoom_out()

        for crossover in self.crossovers_list:
            crossover.on_zoom_out()

        for train_id in self.trains:
            self.trains[train_id].on_zoom_out()

        self.on_change_base_offset(self.view.base_offset)

    def on_save_state(self):
        self.model.on_save_state()
        self.scheduler.on_save_state()
        self.dispatcher.on_save_state()
        for signal in self.signals_list:
            signal.on_save_state()

        for route in self.train_routes_sorted_list:
            route.on_save_state()

        for switch in self.switches_list:
            switch.on_save_state()

        for crossover in self.crossovers_list:
            crossover.on_save_state()

        self.model.on_clear_trains_info()
        for train_id in self.trains:
            self.trains[train_id].on_save_state()

    def on_update_time(self, game_time):
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        for route in self.train_routes_sorted_list:
            route.on_update_time(game_time)

        successful_departure_state = []
        for train_id in self.trains:
            self.trains[train_id].on_update_time(game_time)
            if self.trains[train_id].model.state == 'successful_departure':
                successful_departure_state.append(train_id)

        for train_id in successful_departure_state:
            self.trains[train_id].on_deactivate()
            self.trains.pop(train_id)

        self.scheduler.on_update_time(game_time)
        self.dispatcher.on_update_time(game_time)

    def on_level_up(self, level):
        self.scheduler.on_level_up(level)

    def on_open_schedule(self):
        self.scheduler.on_activate_view()
        self.view.on_deactivate_zoom_buttons()

    @_map_view_is_active
    def on_close_schedule(self):
        self.view.on_activate_zoom_buttons()
        self.view.open_schedule_button.on_activate()

    def on_switch_signal_to_green(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_green()

    def on_switch_signal_to_red(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_red()

    def on_update_train_route_sections(self, track, train_route, last_car_position):
        self.train_routes[track][train_route].on_update_train_route_sections(last_car_position)

    def on_update_train_route_section_status(self, train_route_data, status):
        self.train_routes[train_route_data[0]][train_route_data[1]].on_update_section_status(train_route_data[2],
                                                                                             status)

    def on_train_route_section_force_busy_on(self, section, positions, train_id):
        if section[0] in ('left_railroad_switch', 'right_railroad_switch'):
            self.switches[section[1]][section[2]][section[0]].on_force_busy_on(positions, train_id)

        if section[0] in ('left_crossover', 'right_crossover'):
            self.crossovers[section[1]][section[2]][section[0]].on_force_busy_on(positions, train_id)

    def on_train_route_section_force_busy_off(self, section, positions):
        if section[0] in ('left_railroad_switch', 'right_railroad_switch'):
            self.switches[section[1]][section[2]][section[0]].on_force_busy_off()

        if section[0] in ('left_crossover', 'right_crossover'):
            self.crossovers[section[1]][section[2]][section[0]].on_force_busy_off(positions)

    def on_leave_entry(self, entry_id):
        self.scheduler.on_leave_entry(entry_id)

    def on_leave_track(self, track):
        self.dispatcher.on_leave_track(track)

    def on_update_train_route_priority(self, track, train_route, priority):
        self.train_routes[track][train_route].on_update_priority(priority)

    def on_set_trail_points(self, train_id, trail_points_v2):
        self.trains[train_id].on_set_trail_points(trail_points_v2)

    def on_set_train_start_point(self, train_id, first_car_start_point):
        self.trains[train_id].on_set_train_start_point(first_car_start_point)

    def on_set_train_stop_point(self, train_id, first_car_stop_point):
        self.trains[train_id].on_set_train_stop_point(first_car_stop_point)

    def on_set_train_destination_point(self, train_id, first_car_destination_point):
        self.trains[train_id].on_set_train_destination_point(first_car_destination_point)

    def on_open_train_route(self, track, train_route, train_id, cars):
        self.train_routes[track][train_route].on_open_train_route(train_id, cars)

    def on_close_train_route(self, track, train_route):
        self.train_routes[track][train_route].on_close_train_route()

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        train = self.model.on_create_train(train_id, cars, track, train_route, state, direction, new_direction,
                                           current_direction, priority, boarding_time, exp, money)
        train.view.on_change_base_offset(self.view.base_offset)
        train.view.on_change_screen_resolution(self.view.screen_resolution)
        train.view.on_change_zoom_factor(self.view.zoom_factor, zoom_out_activated=self.view.zoom_out_activated)
        self.trains[train.train_id] = train
        self.dispatcher.on_add_train(train)
        train.parent_controller.on_open_train_route(track, train_route, train_id, cars)
        train.on_activate()
        if not self.view.is_activated:
            train.on_deactivate_view()

