from logging import getLogger
from operator import attrgetter

from controller import *
from ui.fade_animation.fade_in_animation.map_fade_in_animation import MapFadeInAnimation
from ui.fade_animation.fade_out_animation.map_fade_out_animation import MapFadeOutAnimation


class MapController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = MapFadeInAnimation(self.view)
        self.fade_out_animation = MapFadeOutAnimation(self.view)
        self.scheduler = self.create_scheduler()
        self.constructor = self.create_constructor()
        self.dispatcher = self.create_dispatcher()
        self.mini_map = self.create_mini_map()
        self.narrator = self.create_narrator()
        self.signals, self.signals_list = self.create_signals()
        self.train_routes, self.train_routes_sorted_list = self.create_train_routes()
        self.switches, self.switches_list = self.create_switches()
        self.crossovers, self.crossovers_list = self.create_crossovers()
        self.trains, self.trains_list = self.create_trains()
        self.shops = self.create_shops()
        self.lifecycle_ended_trains = []
        self.fade_in_animation.constructor_fade_in_animation = self.constructor.fade_in_animation
        self.fade_in_animation.scheduler_fade_in_animation = self.scheduler.fade_in_animation
        self.fade_in_animation.dispatcher_fade_in_animation = self.dispatcher.fade_in_animation
        self.fade_in_animation.mini_map_fade_in_animation = self.mini_map.fade_in_animation
        self.fade_in_animation.narrator_fade_in_animation = self.narrator.fade_in_animation
        self.fade_out_animation.constructor_fade_out_animation = self.constructor.fade_out_animation
        self.fade_out_animation.scheduler_fade_out_animation = self.scheduler.fade_out_animation
        self.fade_out_animation.dispatcher_fade_out_animation = self.dispatcher.fade_out_animation
        self.fade_out_animation.mini_map_fade_out_animation = self.mini_map.fade_out_animation
        self.fade_out_animation.narrator_fade_out_animation = self.narrator.fade_out_animation
        for signal in self.signals_list:
            self.fade_in_animation.signal_fade_in_animations.append(signal.fade_in_animation)
            self.fade_out_animation.signal_fade_out_animations.append(signal.fade_out_animation)

        for switch in self.switches_list:
            self.fade_in_animation.railroad_switch_fade_in_animations.append(switch.fade_in_animation)
            self.fade_out_animation.railroad_switch_fade_out_animations.append(switch.fade_out_animation)

        for crossover in self.crossovers_list:
            self.fade_in_animation.crossover_fade_in_animations.append(crossover.fade_in_animation)
            self.fade_out_animation.crossover_fade_out_animations.append(crossover.fade_out_animation)

        for train_route in self.train_routes_sorted_list:
            self.fade_in_animation.train_route_fade_in_animations.append(train_route.fade_in_animation)
            self.fade_out_animation.train_route_fade_out_animations.append(train_route.fade_out_animation)
            if train_route.model.opened:
                self.on_set_trail_points(train_route.model.last_opened_by, train_route.model.trail_points_v2)

        for train in self.trains_list:
            train.on_train_setup()
            self.fade_in_animation.train_fade_in_animations.append(train.fade_in_animation)
            self.fade_out_animation.train_fade_out_animations.append(train.fade_out_animation)
            if train.model.state in ('approaching', 'approaching_pass_through'):
                self.dispatcher.on_add_train(train)

        for shop in self.shops:
            self.fade_in_animation.shop_fade_in_animations.append(shop.fade_in_animation)
            self.fade_out_animation.shop_fade_out_animations.append(shop.fade_out_animation)

        self.child_controllers = [
            self.scheduler, self.constructor, self.dispatcher, self.mini_map, self.narrator,
            *self.signals_list, *self.train_routes_sorted_list,
            *self.switches_list, *self.crossovers_list, *self.trains_list, *self.shops
        ]
        self.map_element_controllers = [
            self.mini_map, *self.signals_list, *self.train_routes_sorted_list,
            *self.switches_list, *self.crossovers_list, *self.trains_list
        ]

    @abstractmethod
    def create_scheduler(self):
        pass

    @abstractmethod
    def create_constructor(self):
        pass

    @abstractmethod
    def create_dispatcher(self):
        pass

    @abstractmethod
    def create_mini_map(self):
        pass

    @abstractmethod
    def create_narrator(self):
        pass

    @abstractmethod
    def create_signals(self):
        pass

    @abstractmethod
    def create_train_routes(self):
        pass

    @abstractmethod
    def create_switches(self):
        pass

    @abstractmethod
    def create_crossovers(self):
        pass

    @abstractmethod
    def create_trains(self):
        pass

    @abstractmethod
    def create_shops(self):
        pass

    @final
    def on_save_state(self):
        # before writing new train state to the database
        # previous data should be cleared to remove old trains
        self.model.on_clear_trains_info()
        super().on_save_state()

    @final
    def on_update_time(self, dt):
        # train routes are sorted by priority to implement some kind of queue
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        super().on_update_time(dt)
        # collected trains which has departed successfully should be removed from the game
        for train in self.lifecycle_ended_trains:
            train.view.on_deactivate()
            train.view.on_update_opacity(0)
            train.view.on_detach_window_handlers()
            self.fade_in_animation.train_fade_in_animations.remove(train.fade_in_animation)
            self.fade_out_animation.train_fade_out_animations.remove(train.fade_out_animation)
            self.trains.pop(train.train_id)
            self.trains_list.remove(train)
            self.child_controllers.remove(train)
            self.map_element_controllers.remove(train)

        self.lifecycle_ended_trains.clear()

    @final
    def on_save_and_commit_last_known_zoom(self):
        self.model.on_save_and_commit_last_known_zoom()

    @final
    def on_unlock(self):
        super().on_unlock()
        self.scheduler.on_unlock()
        for track in range(self.model.unlocked_tracks_by_default):
            self.on_unlock_track(track + 1)
            self.constructor.on_remove_track_from_matrix(track + 1)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)
        self.constructor.on_unlock_track(track)
        self.scheduler.on_unlock_track(track)
        self.dispatcher.on_unlock_track(track)
        self.mini_map.on_unlock_track(track)
        for track_param, base_route in self.model.get_signals_to_unlock_with_track(track):
            self.signals[track_param][base_route].on_unlock()

        for track_param_1, track_param_2, switch_type in self.model.get_switches_to_unlock_with_track(track):
            self.switches[track_param_1][track_param_2][switch_type].on_unlock()

        for track_param_1, track_param_2, crossover_type in self.model.get_crossovers_to_unlock_with_track(track):
            self.crossovers[track_param_1][track_param_2][crossover_type].on_unlock()

        if self.view.map_move_mode_available:
            for shop_id in self.model.get_shops_to_unlock_with_track(track):
                self.view.shop_buttons[shop_id[0]].on_activate()

    @final
    def on_unlock_environment(self, tier):
        self.model.on_unlock_environment(tier)
        self.scheduler.on_unlock_environment(tier)
        self.mini_map.on_unlock_environment(tier)
        for track_param, base_route in self.model.get_signals_to_unlock_with_environment(tier):
            self.signals[track_param][base_route].on_unlock()

        for track_param_1, track_param_2, switch_type in self.model.get_switches_to_unlock_with_environment(tier):
            self.switches[track_param_1][track_param_2][switch_type].on_unlock()

        for track_param_1, track_param_2, crossover_type in self.model.get_crossovers_to_unlock_with_environment(tier):
            self.crossovers[track_param_1][track_param_2][crossover_type].on_unlock()

    @final
    def on_open_schedule(self):
        # Constructor and Scheduler views cannot be activated at the same time;
        # when user opens schedule screen it means constructor screen has to be closed
        # before schedule screen is opened
        for shop in self.shops:
            shop.fade_out_animation.on_activate()

        if self.constructor.view.is_activated:
            self.view.on_close_constructor()
            self.constructor.fade_out_animation.on_activate()

        self.scheduler.fade_in_animation.on_activate()
        self.view.on_deactivate_shop_buttons()
        self.parent_controller.on_deactivate_map_switcher_button()
        self.parent_controller.on_force_close_map_switcher()
        # if mini map is active when user opens schedule screen, it should also be hidden
        self.on_deactivate_mini_map()

    @final
    def on_open_constructor(self):
        # Constructor and Scheduler views cannot be activated at the same time;
        # when user opens constructor screen it means schedule screen has to be closed
        # before constructor screen is opened
        for shop in self.shops:
            shop.fade_out_animation.on_activate()

        if self.scheduler.view.is_activated:
            self.view.on_close_schedule()
            self.scheduler.fade_out_animation.on_activate()

        self.constructor.fade_in_animation.on_activate()
        self.view.on_deactivate_shop_buttons()
        self.parent_controller.on_deactivate_map_switcher_button()
        self.parent_controller.on_force_close_map_switcher()
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.on_deactivate_mini_map()

    @final
    def on_close_schedule(self):
        self.view.on_close_schedule()
        self.parent_controller.on_activate_map_switcher_button()

    @final
    def on_close_constructor(self):
        self.view.on_close_constructor()
        self.parent_controller.on_activate_map_switcher_button()

    @final
    def on_switch_signal_to_green(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_green()

    @final
    def on_switch_signal_to_red(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_red()

    @final
    def on_update_train_route_sections(self, track, train_route, last_car_position):
        self.train_routes[track][train_route].on_update_train_route_sections(last_car_position)

    @final
    def on_update_train_route_section_status(self, train_route_data, status):
        self.train_routes[
            train_route_data[TRAIN_ROUTE_DATA_TRACK_NUMBER]
        ][
            train_route_data[TRAIN_ROUTE_DATA_TYPE]
        ].on_update_section_status(train_route_data[TRAIN_ROUTE_DATA_SECTION_NUMBER], status)

    @final
    def on_train_route_section_force_busy_on(self, section, positions, train_id):
        if section[SECTION_TYPE] in ('left_railroad_switch', 'right_railroad_switch'):
            self.switches[
                section[SECTION_TRACK_NUMBER_1]
            ][
                section[SECTION_TRACK_NUMBER_2]
            ][
                section[SECTION_TYPE]
            ].on_force_busy_on(positions, train_id)

        if section[SECTION_TYPE] in ('left_crossover', 'right_crossover'):
            self.crossovers[
                section[SECTION_TRACK_NUMBER_1]
            ][
                section[SECTION_TRACK_NUMBER_2]
            ][
                section[SECTION_TYPE]
            ].on_force_busy_on(positions, train_id)

    @final
    def on_train_route_section_force_busy_off(self, section, positions):
        if section[SECTION_TYPE] in ('left_railroad_switch', 'right_railroad_switch'):
            self.switches[
                section[SECTION_TRACK_NUMBER_1]
            ][
                section[SECTION_TRACK_NUMBER_2]
            ][
                section[SECTION_TYPE]
            ].on_force_busy_off()

        if section[SECTION_TYPE] in ('left_crossover', 'right_crossover'):
            self.crossovers[
                section[SECTION_TRACK_NUMBER_1]
            ][
                section[SECTION_TRACK_NUMBER_2]
            ][
                section[SECTION_TYPE]
            ].on_force_busy_off(positions)

    @final
    def on_leave_entry(self, entry_id):
        self.scheduler.on_leave_entry(entry_id)

    @final
    def on_leave_track(self, track):
        self.dispatcher.on_leave_track(track)

    @final
    def on_update_train_route_priority(self, track, train_route, priority):
        self.train_routes[track][train_route].on_update_priority(priority)

    @final
    def on_set_trail_points(self, train_id, trail_points_v2):
        self.trains[train_id].on_set_trail_points(trail_points_v2)

    @final
    def on_set_train_start_point(self, train_id, first_car_start_point):
        self.trains[train_id].on_set_train_start_point(first_car_start_point)

    @final
    def on_set_train_stop_point(self, train_id, first_car_stop_point):
        self.trains[train_id].on_set_train_stop_point(first_car_stop_point)

    @final
    def on_set_train_destination_point(self, train_id, first_car_destination_point):
        self.trains[train_id].on_set_train_destination_point(first_car_destination_point)

    @final
    def on_open_train_route(self, track, train_route, train_id, cars):
        self.train_routes[track][train_route].on_open_train_route(train_id, cars)

    @final
    def on_close_train_route(self, track, train_route):
        self.train_routes[track][train_route].on_close_train_route()

    @final
    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money, switch_direction_required):
        train = self.model.on_create_train(train_id, cars, track, train_route, state, direction, new_direction,
                                           current_direction, priority, boarding_time, exp, money,
                                           switch_direction_required)
        train.view.on_window_resize(*self.view.screen_resolution)
        # add new train to the list and dictionary
        self.trains[train_id] = train
        self.trains_list.append(train)
        self.child_controllers.append(train)
        self.map_element_controllers.append(train)
        # add new train to the dispatcher
        self.dispatcher.on_add_train(train)
        self.on_open_train_route(track, train_route, train_id, cars)
        if self.view.is_activated:
            train.fade_in_animation.on_activate()
        else:
            train.fade_out_animation.on_activate()

    @final
    def on_save_and_commit_last_known_base_offset(self):
        self.model.on_save_and_commit_last_known_base_offset()

    @final
    def on_open_shop_details(self, shop_id):
        self.shops[shop_id].fade_in_animation.on_activate()
        self.view.on_deactivate_shop_buttons()
        self.mini_map.fade_out_animation.on_activate()

    @final
    def on_close_shop_details(self, shop_id):
        self.shops[shop_id].fade_out_animation.on_activate()
        self.view.on_activate_shop_buttons()

    @final
    def on_train_lifecycle_ended(self, train):
        self.lifecycle_ended_trains.append(train)

    @final
    def on_map_move_mode_available(self):
        self.view.on_map_move_mode_available()

    @final
    def on_map_move_mode_unavailable(self):
        self.view.on_map_move_mode_unavailable()

    @final
    def on_open_map_switcher(self):
        for shop in self.shops:
            shop.fade_out_animation.on_activate()

        self.view.on_deactivate_shop_buttons()
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.on_deactivate_mini_map()

    @final
    def on_close_map_switcher(self):
        self.view.on_close_map_switcher()

    @final
    def on_deactivate_money_target(self):
        self.constructor.on_deactivate_money_target()

    @final
    def on_activate_mini_map(self):
        self.mini_map.fade_in_animation.on_activate()

    @final
    def on_deactivate_mini_map(self):
        self.mini_map.fade_out_animation.on_activate()

    @final
    def on_announcement_add(self, announcement_time, announcement_type, arguments):
        self.narrator.on_announcement_add(announcement_time, announcement_type, arguments)
