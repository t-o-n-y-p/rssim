from logging import getLogger
from operator import attrgetter
from typing import Dict, List

from controller import *
from model.map_model import MapModel
from view.map_view import MapView
from controller.scheduler_controller import SchedulerController
from controller.constructor_controller import ConstructorController
from controller.dispatcher_controller import DispatcherController
from controller.signal_controller import SignalController
from controller.train_route_controller import TrainRouteController
from controller.railroad_switch_controller import RailroadSwitchController
from controller.crossover_controller import CrossoverController
from controller.train_controller import TrainController
from controller.shop_controller import ShopController
from ui.fade_animation.fade_in_animation.map_fade_in_animation import MapFadeInAnimation
from ui.fade_animation.fade_out_animation.map_fade_out_animation import MapFadeOutAnimation


class MapController(MapBaseController):
    def __init__(self, model: MapModel, view: MapView, scheduler: SchedulerController,
                 constructor: ConstructorController, dispatcher: DispatcherController,
                 signals: Dict[int, Dict[str, SignalController]], signals_list: List[SignalController],
                 train_routes: Dict[int, Dict[str, TrainRouteController]],
                 train_routes_sorted_list: List[TrainRouteController],
                 switches: Dict[int, Dict[int, Dict[str, RailroadSwitchController]]],
                 switches_list: List[RailroadSwitchController],
                 crossovers: Dict[int, Dict[int, Dict[str, CrossoverController]]],
                 crossovers_list: List[CrossoverController],
                 trains: Dict[int, TrainController], trains_list: List[TrainController], shops: List[ShopController],
                 map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.controller'))
        self.map_id = map_id
        self.fade_in_animation = MapFadeInAnimation(self)
        self.fade_out_animation = MapFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()
        self.scheduler = scheduler
        self.constructor = constructor
        self.dispatcher = dispatcher
        self.signals = signals
        self.signals_list = signals_list
        self.train_routes = train_routes
        self.train_routes_sorted_list = train_routes_sorted_list
        self.switches = switches
        self.switches_list = switches_list
        self.crossovers = crossovers
        self.crossovers_list = crossovers_list
        self.trains = trains
        self.trains_list = trains_list
        self.lifecycle_ended_trains = []
        self.shops = shops
        self.fade_in_animation.constructor_fade_in_animation = self.constructor.fade_in_animation
        self.fade_in_animation.scheduler_fade_in_animation = self.scheduler.fade_in_animation
        self.fade_in_animation.dispatcher_fade_in_animation = self.dispatcher.fade_in_animation
        self.fade_out_animation.constructor_fade_out_animation = self.constructor.fade_out_animation
        self.fade_out_animation.scheduler_fade_out_animation = self.scheduler.fade_out_animation
        self.fade_out_animation.dispatcher_fade_out_animation = self.dispatcher.fade_out_animation
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
            self.scheduler, self.constructor, self.dispatcher, *self.signals_list, *self.train_routes_sorted_list,
            *self.switches_list, *self.crossovers_list, *self.trains_list, *self.shops
        ]
        self.map_element_controllers = [
            *self.signals_list, *self.train_routes_sorted_list,
            *self.switches_list, *self.crossovers_list, *self.trains_list
        ]

    def create_map_elements(self):
        pass

    @final
    def on_change_screen_resolution(self, screen_resolution):
        # recalculating base offset before applying new screen resolution
        self.view.on_recalculate_base_offset_for_new_screen_resolution(screen_resolution)
        super().on_change_screen_resolution(screen_resolution)
        self.view.check_base_offset_limits()
        self.on_save_and_commit_last_known_base_offset(self.view.base_offset)
        self.on_change_base_offset(self.view.base_offset)

    @final
    def on_save_state(self):
        # before writing new train state to the database
        # previous data should be cleared to remove old trains
        self.model.on_clear_trains_info()
        super().on_save_state()

    @final
    def on_update_time(self):
        # train routes are sorted by priority to implement some kind of queue
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        super().on_update_time()
        # collected trains which has departed successfully should be removed from the game
        for train in self.lifecycle_ended_trains:
            train.on_deactivate_view()
            train.view.on_update_opacity(0)
            self.fade_in_animation.train_fade_in_animations.remove(train.fade_in_animation)
            self.fade_out_animation.train_fade_out_animations.remove(train.fade_out_animation)
            self.trains.pop(train.train_id)
            self.trains_list.remove(train)
            self.child_controllers.remove(train)
            self.map_element_controllers.remove(train)

        self.lifecycle_ended_trains.clear()

    @final
    def on_zoom_in(self):
        super().on_zoom_in()
        self.on_change_base_offset(self.view.base_offset)
        self.model.on_save_and_commit_zoom_out_activated(False)

    @final
    def on_zoom_out(self):
        super().on_zoom_out()
        self.on_change_base_offset(self.view.base_offset)
        self.model.on_save_and_commit_zoom_out_activated(True)

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
        # if schedule screen is opened, zoom in/zoom out buttons should also be hidden
        self.view.on_deactivate_zoom_buttons()
        self.view.on_deactivate_shop_buttons()
        self.parent_controller.on_deactivate_map_switcher_button()
        self.parent_controller.on_force_close_map_switcher()
        # if mini map is active when user opens schedule screen, it should also be hidden
        self.view.is_mini_map_activated = False

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
        # if constructor screen is opened, zoom in/zoom out buttons should also be hidden
        self.view.on_deactivate_zoom_buttons()
        self.view.on_deactivate_shop_buttons()
        self.parent_controller.on_deactivate_map_switcher_button()
        self.parent_controller.on_force_close_map_switcher()
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.view.is_mini_map_activated = False

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
        train.view.on_change_screen_resolution(self.view.screen_resolution)
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

        if self.view.map_move_mode:
            train.view.on_change_base_offset(self.view.base_offset)

    @final
    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.constructor.on_change_feature_unlocked_notification_state(notification_state)

    @final
    def on_change_construction_completed_notification_state(self, notification_state):
        self.constructor.on_change_construction_completed_notification_state(notification_state)

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        for shop in self.shops:
            shop.on_change_shop_storage_notification_state(notification_state)

    @final
    def on_save_and_commit_last_known_base_offset(self, base_offset):
        self.model.on_save_and_commit_last_known_base_offset(base_offset)

    @final
    def on_open_shop_details(self, shop_id):
        self.shops[shop_id].fade_in_animation.on_activate()
        self.view.on_deactivate_zoom_buttons()
        self.view.on_deactivate_shop_buttons()
        self.view.is_mini_map_activated = False

    @final
    def on_close_shop_details(self, shop_id):
        self.shops[shop_id].fade_out_animation.on_activate()
        self.view.on_activate_zoom_buttons()
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

        self.view.on_deactivate_zoom_buttons()
        self.view.on_deactivate_shop_buttons()
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.view.is_mini_map_activated = False

    def on_close_map_switcher(self):
        self.view.on_close_map_switcher()

    def on_deactivate_money_target(self):
        self.constructor.on_deactivate_money_target()
