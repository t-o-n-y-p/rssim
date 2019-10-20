from logging import getLogger
from operator import attrgetter

from controller import *


class MapController(AppBaseController, GameBaseController):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.controller'))
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
        self.trains_list = []
        self.shops = []
        self.map_id = map_id

    @final
    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()
        self.scheduler.on_update_view()
        self.dispatcher.on_update_view()
        self.constructor.on_update_view()
        for signal in self.signals_list:
            signal.on_update_view()

        for route in self.train_routes_sorted_list:
            route.on_update_view()

        for switch in self.switches_list:
            switch.on_update_view()

        for crossover in self.crossovers_list:
            crossover.on_update_view()

        for train in self.trains_list:
            train.on_update_view()

        for shop in self.shops:
            shop.on_update_view()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_recalculate_base_offset_for_new_screen_resolution(screen_resolution)
        self.view.on_change_screen_resolution(screen_resolution)
        self.scheduler.on_change_screen_resolution(screen_resolution)
        self.dispatcher.on_change_screen_resolution(screen_resolution)
        self.constructor.on_change_screen_resolution(screen_resolution)
        for signal in self.signals_list:
            signal.on_change_screen_resolution(screen_resolution)

        for route in self.train_routes_sorted_list:
            route.on_change_screen_resolution(screen_resolution)

        for switch in self.switches_list:
            switch.on_change_screen_resolution(screen_resolution)

        for crossover in self.crossovers_list:
            crossover.on_change_screen_resolution(screen_resolution)

        for train in self.trains_list:
            train.on_change_screen_resolution(screen_resolution)

        for shop in self.shops:
            shop.on_change_screen_resolution(screen_resolution)

        self.view.check_base_offset_limits()
        self.on_save_and_commit_last_known_base_offset(self.view.base_offset)
        self.on_change_base_offset(self.view.base_offset)

    @final
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

        for train in self.trains_list:
            train.on_change_base_offset(new_base_offset)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)
        self.scheduler.on_unlock_track(track)
        self.dispatcher.on_unlock_track(track)
        for track_param, base_route in self.model.get_signals_to_unlock_with_track(track):
            self.signals[track_param][base_route].on_unlock()

        for track_param_1, track_param_2, switch_type in self.model.get_switches_to_unlock_with_track(track):
            self.switches[track_param_1][track_param_2][switch_type].on_unlock()

        for track_param_1, track_param_2, crossover_type in self.model.get_crossovers_to_unlock_with_track(track):
            self.crossovers[track_param_1][track_param_2][crossover_type].on_unlock()

        if self.view.is_activated:
            for shop_id in self.model.get_shops_to_unlock_with_track(track):
                self.view.shop_buttons[shop_id[0]].on_activate()

        self.view.on_unlock_construction()

    @final
    def on_unlock_environment(self, tier):
        self.model.on_unlock_environment(tier)
        for track_param, base_route in self.model.get_signals_to_unlock_with_environment(tier):
            self.signals[track_param][base_route].on_unlock()

        for track_param_1, track_param_2, switch_type in self.model.get_switches_to_unlock_with_environment(tier):
            self.switches[track_param_1][track_param_2][switch_type].on_unlock()

        for track_param_1, track_param_2, crossover_type in self.model.get_crossovers_to_unlock_with_environment(tier):
            self.crossovers[track_param_1][track_param_2][crossover_type].on_unlock()

        self.view.on_unlock_construction()

    @final
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

        for train in self.trains_list:
            train.on_activate_view()

    @final
    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.scheduler.on_deactivate_view()
        self.constructor.on_deactivate_view()
        self.dispatcher.on_deactivate_view()
        for signal in self.signals_list:
            signal.on_deactivate_view()

        for route in self.train_routes_sorted_list:
            route.on_deactivate_view()

        for switch in self.switches_list:
            switch.on_deactivate_view()

        for crossover in self.crossovers_list:
            crossover.on_deactivate_view()

        for train in self.trains_list:
            train.on_deactivate_view()

        for shop in self.shops:
            shop.on_deactivate_view()

    @final
    def on_zoom_in(self):
        self.model.on_save_and_commit_zoom_out_activated(False)
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)
        for signal in self.signals_list:
            signal.on_zoom_in()

        for route in self.train_routes_sorted_list:
            route.on_zoom_in()

        for switch in self.switches_list:
            switch.on_zoom_in()

        for crossover in self.crossovers_list:
            crossover.on_zoom_in()

        for train in self.trains_list:
            train.on_zoom_in()

        self.on_change_base_offset(self.view.base_offset)

    @final
    def on_zoom_out(self):
        self.model.on_save_and_commit_zoom_out_activated(True)
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)
        for signal in self.signals_list:
            signal.on_zoom_out()

        for route in self.train_routes_sorted_list:
            route.on_zoom_out()

        for switch in self.switches_list:
            switch.on_zoom_out()

        for crossover in self.crossovers_list:
            crossover.on_zoom_out()

        for train in self.trains_list:
            train.on_zoom_out()

        self.on_change_base_offset(self.view.base_offset)

    @final
    def on_save_state(self):
        self.model.on_save_state()
        self.scheduler.on_save_state()
        self.dispatcher.on_save_state()
        self.constructor.on_save_state()
        for signal in self.signals_list:
            signal.on_save_state()

        for route in self.train_routes_sorted_list:
            route.on_save_state()

        for switch in self.switches_list:
            switch.on_save_state()

        for crossover in self.crossovers_list:
            crossover.on_save_state()

        # before writing new train state to the database
        # previous data should be cleared to remove old trains
        self.model.on_clear_trains_info()
        for train in self.trains_list:
            train.on_save_state()

        for shop in self.shops:
            shop.on_save_state()

    @final
    def on_update_time(self):
        super().on_update_time()
        # train routes are sorted by priority to implement some kind of queue
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        for route in self.train_routes_sorted_list:
            route.on_update_time()

        # since dictionary items cannot be removed right inside "for" statement,
        # collect trains which has departed successfully and should be removed from the game
        successful_departure_state = []
        for train in self.trains_list:
            train.on_update_time()
            if train.model.state == 'successful_departure':
                successful_departure_state.append(train.train_id)

        for train_id in successful_departure_state:
            self.trains[train_id].on_deactivate_view()
            self.trains[train_id].view.on_update_opacity(0)
            self.fade_in_animation.train_fade_in_animations.remove(self.trains[train_id].fade_in_animation)
            self.fade_out_animation.train_fade_out_animations.remove(self.trains[train_id].fade_out_animation)
            self.trains_list.remove(self.trains.pop(train_id))

        self.scheduler.on_update_time()
        self.dispatcher.on_update_time()
        self.constructor.on_update_time()
        for shop in self.shops:
            shop.on_update_time()

    @final
    def on_level_up(self, level):
        self.scheduler.on_level_up(level)
        self.constructor.on_level_up(level)
        for shop in self.shops:
            shop.on_level_up(level)

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
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.view.is_mini_map_activated = False

    @final
    def on_close_schedule(self):
        self.view.on_close_schedule()

    @final
    def on_close_constructor(self):
        self.view.on_close_constructor()

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
    def on_set_trail_points(self, train_id, trail_points_v2_head_tail, trail_points_v2_mid):
        self.trains[train_id].on_set_trail_points(trail_points_v2_head_tail, trail_points_v2_mid)

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
                        current_direction, priority, boarding_time, exp, money):
        train = self.model.on_create_train(train_id, cars, track, train_route, state, direction, new_direction,
                                           current_direction, priority, boarding_time, exp, money)
        train.view.on_change_screen_resolution(self.view.screen_resolution)
        # add new train to the list and dictionary
        self.trains[train.train_id] = train
        self.trains_list.append(train)
        # add new train to the dispatcher
        self.dispatcher.on_add_train(train)
        train.parent_controller.on_open_train_route(track, train_route, train_id, cars)
        if self.view.is_activated:
            train.fade_in_animation.on_activate()
        else:
            train.fade_out_animation.on_activate()

        if self.view.map_move_mode:
            train.view.on_change_base_offset(self.view.base_offset)

    @final
    def on_add_money(self, money):
        self.constructor.on_add_money(money)
        for shop in self.shops:
            shop.on_add_money(money)

    @final
    def on_pay_money(self, money):
        self.constructor.on_pay_money(money)
        for shop in self.shops:
            shop.on_pay_money(money)

    @final
    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)
        self.scheduler.on_update_current_locale(new_locale)
        self.dispatcher.on_update_current_locale(new_locale)
        self.constructor.on_update_current_locale(new_locale)
        for signal in self.signals_list:
            signal.on_update_current_locale(new_locale)

        for route in self.train_routes_sorted_list:
            route.on_update_current_locale(new_locale)

        for switch in self.switches_list:
            switch.on_update_current_locale(new_locale)

        for crossover in self.crossovers_list:
            crossover.on_update_current_locale(new_locale)

        for train in self.trains_list:
            train.on_update_current_locale(new_locale)

        for shop in self.shops:
            shop.on_update_current_locale(new_locale)

    @final
    def on_disable_notifications(self):
        self.view.on_disable_notifications()
        self.scheduler.on_disable_notifications()
        self.dispatcher.on_disable_notifications()
        self.constructor.on_disable_notifications()
        for signal in self.signals_list:
            signal.on_disable_notifications()

        for route in self.train_routes_sorted_list:
            route.on_disable_notifications()

        for switch in self.switches_list:
            switch.on_disable_notifications()

        for crossover in self.crossovers_list:
            crossover.on_disable_notifications()

        for train in self.trains_list:
            train.on_disable_notifications()

        for shop in self.shops:
            shop.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        self.view.on_enable_notifications()
        self.scheduler.on_enable_notifications()
        self.dispatcher.on_enable_notifications()
        self.constructor.on_enable_notifications()
        for signal in self.signals_list:
            signal.on_enable_notifications()

        for route in self.train_routes_sorted_list:
            route.on_enable_notifications()

        for switch in self.switches_list:
            switch.on_enable_notifications()

        for crossover in self.crossovers_list:
            crossover.on_enable_notifications()

        for train in self.trains_list:
            train.on_enable_notifications()

        for shop in self.shops:
            shop.on_enable_notifications()

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
    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()
        self.constructor.on_apply_shaders_and_draw_vertices()
        self.scheduler.on_apply_shaders_and_draw_vertices()
        for shop in self.shops:
            shop.on_apply_shaders_and_draw_vertices()

    @final
    def on_save_and_commit_last_known_base_offset(self, base_offset):
        self.model.on_save_and_commit_last_known_base_offset(base_offset)

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        self.scheduler.on_update_fade_animation_state(new_state)
        self.constructor.on_update_fade_animation_state(new_state)
        self.dispatcher.on_update_fade_animation_state(new_state)
        for signal in self.signals_list:
            signal.on_update_fade_animation_state(new_state)

        for switch in self.switches_list:
            switch.on_update_fade_animation_state(new_state)

        for crossover in self.crossovers_list:
            crossover.on_update_fade_animation_state(new_state)

        for train in self.trains_list:
            train.on_update_fade_animation_state(new_state)

        for shop in self.shops:
            shop.on_update_fade_animation_state(new_state)

    @final
    def on_update_clock_state(self, clock_24h_enabled):
        self.scheduler.on_update_clock_state(clock_24h_enabled)

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
