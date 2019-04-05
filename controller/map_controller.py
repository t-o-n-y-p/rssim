from operator import attrgetter
from logging import getLogger

from controller import *


class MapController(Controller):
    """
    Implements Map controller.
    Map object is responsible for properties, UI and events related to the map.
    """
    def __init__(self, game_controller):
        """
        Properties:
            scheduler                           Scheduler object controller
            constructor                         Constructor object controller
            dispatcher                          Dispatcher object controller
            signals                             2-level dictionary of Signal object controllers
            signals_list                        list of Signal object controllers
            train_routes                        2-level dictionary of Train route object controllers
            train_routes_sorted_list            list of Train route object controllers
            switches                            3-level dictionary of Railroad switch object controllers
            switches_list                       list of Railroad switch object controllers
            crossovers                          3-level dictionary of Crossover object controllers
            crossovers_list                     list of Crossover object controllers
            trains                              dictionary of Train object controllers
            trains_list                         list of Train object controllers

        :param game_controller:                 Game controller (parent controller)
        """
        super().__init__(parent_controller=game_controller, logger=getLogger('root.app.game.map.controller'))
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

    def on_update_view(self):
        """
        Notifies the view and all child views to update fade-in/fade-out animations
        and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.view.on_update()
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

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Map object: controller and model. Model activates the view if necessary.
        Also activates all child objects.
        """
        self.is_activated = True
        self.model.on_activate()
        self.scheduler.on_activate()
        self.dispatcher.on_activate()
        self.constructor.on_activate()
        for signal in self.signals_list:
            signal.on_activate()

        for route in self.train_routes_sorted_list:
            route.on_activate()

        for switch in self.switches_list:
            switch.on_activate()

        for crossover in self.crossovers_list:
            crossover.on_activate()

        for train in self.trains_list:
            train.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.scheduler.on_deactivate()
        self.dispatcher.on_deactivate()
        self.constructor.on_deactivate()
        for signal in self.signals_list:
            signal.on_deactivate()

        for route in self.train_routes_sorted_list:
            route.on_deactivate()

        for switch in self.switches_list:
            switch.on_deactivate()

        for crossover in self.crossovers_list:
            crossover.on_deactivate()

        for train in self.trains_list:
            train.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.
        Note that adjusting base offset is made by on_change_base_offset handler,
        which is called after screen resolution is updated.

        :param screen_resolution:       new screen resolution
        """
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

        self.on_change_base_offset(self.view.base_offset)

    def on_change_base_offset(self, new_base_offset):
        """
        Notifies the view and all child controllers about base offset update.

        :param new_base_offset:         new base offset
        """
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

    def on_unlock_track(self, track):
        """
        Notifies the model, the Scheduler, Dispatcher controllers
        and the corresponding Signal controllers the track is unlocked.

        :param track:                   track number
        """
        self.model.on_unlock_track(track)
        self.scheduler.on_unlock_track(track)
        self.dispatcher.on_unlock_track(track)
        for (track_param, base_route) in self.model.get_signals_to_unlock_with_track(track):
            self.signals[track_param][base_route].on_unlock()

        for (track_param_1, track_param_2, switch_type) in self.model.get_switches_to_unlock_with_track(track):
            self.switches[track_param_1][track_param_2][switch_type].on_unlock()

        for (track_param_1, track_param_2, crossover_type) in self.model.get_crossovers_to_unlock_with_track(track):
            self.crossovers[track_param_1][track_param_2][crossover_type].on_unlock()

    def on_unlock_environment(self, tier):
        """
        Notifies the model that given environment tier is unlocked,

        :param tier:                    environment tier number
        """
        self.model.on_unlock_environment(tier)

    def on_activate_view(self):
        """
        Activates the view and all Signal, Train route, Railroad switch, Crossover, Train views
        if user opened game screen in the app.
        """
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

    def on_deactivate_view(self):
        """
        Deactivates the view and child views if user either closed game screen or opened settings screen.
        """
        self.view.on_deactivate()
        self.scheduler.on_deactivate_view()
        self.constructor.on_deactivate_view()
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

    def on_zoom_in(self):
        """
        Notifies the view and all Signal, Train route, Railroad switch, Crossover, Train views to zoom in all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler
        which is called after scale factor is updated.
        """
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

    def on_zoom_out(self):
        """
        Notifies the view and all Signal, Train route, Railroad switch, Crossover, Train views to zoom out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler
        which is called after scale factor is updated.
        """
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

    def on_save_state(self):
        """
        Notifies the model and all child controllers to save state to user progress database.
        """
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

    def on_update_time(self, game_time):
        """
        Notifies all Train route controllers sorted by priority, Train controllers,
        Scheduler, Dispatcher, Constructor controllers about in-game time update.

        :param game_time:               current in-game time
        """
        # train routes are sorted by priority to implement some kind of queue
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        for route in self.train_routes_sorted_list:
            route.on_update_time(game_time)

        # since dictionary items cannot be removed right inside "for" statement,
        # collect trains which has departed successfully and should be removed from the game
        successful_departure_state = []
        for train in self.trains_list:
            train.on_update_time(game_time)
            if train.model.state == 'successful_departure':
                successful_departure_state.append(train.train_id)

        for train_id in successful_departure_state:
            self.trains[train_id].on_deactivate()
            self.trains_list.remove(self.trains.pop(train_id))

        self.scheduler.on_update_time(game_time)
        self.dispatcher.on_update_time(game_time)
        self.constructor.on_update_time(game_time)

    def on_level_up(self, level):
        """
        Notifies the model, the Scheduler and Constructor controllers about level update.

        :param level:                   new level value
        """
        self.scheduler.on_level_up(level)
        self.constructor.on_level_up(level)

    def on_open_schedule(self):
        """
        Activates Scheduler view to open Scheduler screen for player.
        """
        # Constructor and Scheduler views cannot be activated at the same time;
        # when user opens schedule screen it means constructor screen has to be closed
        # before schedule screen is opened
        self.constructor.on_deactivate_view()
        self.on_close_constructor()
        self.scheduler.on_activate_view()
        # if schedule screen is opened, zoom in/zoom out buttons should also be hidden
        self.view.on_deactivate_zoom_buttons()
        # if mini map is active when user opens schedule screen, it should also be hidden
        self.view.is_mini_map_activated = False

    def on_open_constructor(self):
        """
        Activates Constructor view to open Scheduler screen for player.
        """
        # Constructor and Scheduler views cannot be activated at the same time;
        # when user opens constructor screen it means schedule screen has to be closed
        # before constructor screen is opened
        self.scheduler.on_deactivate_view()
        self.on_close_schedule()
        self.constructor.on_activate_view()
        # if constructor screen is opened, zoom in/zoom out buttons should also be hidden
        self.view.on_deactivate_zoom_buttons()
        # if mini map is active when user opens constructor screen, it should also be hidden
        self.view.is_mini_map_activated = False

    @map_view_is_active
    def on_close_schedule(self):
        """
        Activates back all buttons which are hidden when Scheduler view is active:
        zoom in/out buttons and open schedule button.
        """
        self.view.on_activate_zoom_buttons()
        self.view.open_schedule_button.on_activate()

    @map_view_is_active
    def on_close_constructor(self):
        """
        Activates back all buttons which are hidden when Constructor view is active:
        zoom in/out buttons and open constructor button.
        """
        self.view.on_activate_zoom_buttons()
        self.view.open_constructor_button.on_activate()

    def on_switch_signal_to_green(self, signal_track, signal_base_route):
        """
        Notifies particular Signal controller about state change to green.

        :param signal_track:                    signal track code from base route system
        :param signal_base_route:               signal base route type
        """
        self.signals[signal_track][signal_base_route].on_switch_to_green()

    def on_switch_signal_to_red(self, signal_track, signal_base_route):
        """
        Notifies particular Signal controller about state change to red.

        :param signal_track:                    signal track code from base route system
        :param signal_base_route:               signal base route type
        """
        self.signals[signal_track][signal_base_route].on_switch_to_red()

    def on_update_train_route_sections(self, track, train_route, last_car_position):
        """
        Notifies Train route controller about last train car position update.

        :param track:                           train route track number
        :param train_route:                     train route type
        :param last_car_position:               train last car position on the route
        """
        self.train_routes[track][train_route].on_update_train_route_sections(last_car_position)

    def on_update_train_route_section_status(self, train_route_data, status):
        """
        Notifies Train route controller about particular section status update.

        :param train_route_data:                list of train route track number, type and section number
        :param status:                          new status
        """
        self.train_routes[
            train_route_data[TRAIN_ROUTE_DATA_TRACK_NUMBER]
        ][
            train_route_data[TRAIN_ROUTE_DATA_TYPE]
        ].on_update_section_status(train_route_data[TRAIN_ROUTE_DATA_SECTION_NUMBER], status)

    def on_train_route_section_force_busy_on(self, section, positions, train_id):
        """
        Notifies Railroad switch or Crossover controller about force_busy state change to True.

        :param section:                         Railroad switch or Crossover object info: track numbers and type
        :param positions:                       indicates which direction is about to be forced busy
        :param train_id:                        id of the train which is about to pass through
        """
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

    def on_train_route_section_force_busy_off(self, section, positions):
        """
        Notifies Railroad switch or Crossover controller about force_busy state change to False.

        :param section:                         Railroad switch or Crossover object info: track numbers and type
        :param positions:                       indicates which direction is about to be left
        """
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

    def on_leave_entry(self, entry_id):
        """
        Notifies Scheduler controller that entry is ready for new trains approaching.

        :param entry_id:                        entry identification number from 0 to 3
        """
        self.scheduler.on_leave_entry(entry_id)

    def on_leave_track(self, track):
        """
        Notifies the Dispatcher controller the track is clear for any of the next trains.

        :param track:                           track number
        """
        self.dispatcher.on_leave_track(track)

    def on_update_train_route_priority(self, track, train_route, priority):
        """
        Notifies Train route controller about priority update.

        :param track:                           train rout track number
        :param train_route:                     train route type
        :param priority:                        new priority value
        """
        self.train_routes[track][train_route].on_update_priority(priority)

    def on_set_trail_points(self, train_id, trail_points_v2):
        """
        Notifies Train controller about trail points update.

        :param train_id:                        ID of the train to update trail points
        :param trail_points_v2:                 data
        """
        self.trains[train_id].on_set_trail_points(trail_points_v2)

    def on_set_train_start_point(self, train_id, first_car_start_point):
        """
        Notifies Train controller about initial position update.

        :param train_id:                        ID of the train to update initial position
        :param first_car_start_point:           data
        """
        self.trains[train_id].on_set_train_start_point(first_car_start_point)

    def on_set_train_stop_point(self, train_id, first_car_stop_point):
        """
        Notifies Train controller where to stop the train if signal is at danger.

        :param train_id:                        ID of the train to update stop point
        :param first_car_stop_point:            data
        """
        self.trains[train_id].on_set_train_stop_point(first_car_stop_point)

    def on_set_train_destination_point(self, train_id, first_car_destination_point):
        """
        Notifies Train controller about destination point update.
        When train reaches destination point, route is completed.

        :param train_id:                        ID of the train to update destination point
        :param first_car_destination_point:     data
        """
        self.trains[train_id].on_set_train_destination_point(first_car_destination_point)

    def on_open_train_route(self, track, train_route, train_id, cars):
        """
        Notifies Train route controller to open train route.

        :param track:                           train route track number
        :param train_route:                     train route type
        :param train_id:                        ID of the train which opens the train route
        :param cars:                            number of cars in the train
        """
        self.train_routes[track][train_route].on_open_train_route(train_id, cars)

    def on_close_train_route(self, track, train_route):
        """
        Notifies Train route controller to close train route.

        :param track:                           train route track number
        :param train_route:                     train route type
        """
        self.train_routes[track][train_route].on_close_train_route()

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        """
        Notifies the model to create new train, adds new train to the dictionary, list
        and notifies Dispatcher controller to add new train.

        :param train_id:                        train identification number
        :param cars:                            number of cars in the train
        :param track:                           track number (0 for regular entry and 100 for side entry)
        :param train_route:                     train route type (left/right approaching or side_approaching)
        :param state:                           train state: approaching or approaching_pass_through
        :param direction:                       train arrival direction
        :param new_direction:                   train departure direction
        :param current_direction:               train current direction
        :param priority:                        train priority in the queue
        :param boarding_time:                   amount of boarding time left for this train
        :param exp:                             exp gained when boarding finishes
        :param money:                           money gained when boarding finishes
        """
        train = self.model.on_create_train(train_id, cars, track, train_route, state, direction, new_direction,
                                           current_direction, priority, boarding_time, exp, money)
        train.view.on_change_base_offset(self.view.base_offset)
        train.view.on_change_screen_resolution(self.view.screen_resolution)
        train.view.on_change_zoom_factor(self.view.zoom_factor, zoom_out_activated=self.view.zoom_out_activated)
        # add new train to the list and dictionary
        self.trains[train.train_id] = train
        self.trains_list.append(train)
        # add new train to the dispatcher
        self.dispatcher.on_add_train(train)
        train.parent_controller.on_open_train_route(track, train_route, train_id, cars)
        train.on_activate()
        if not self.view.is_activated:
            train.on_deactivate_view()

    def on_add_money(self, money):
        """
        Notifies Constructor controller about bank account state change when user gains money.

        :param money:                   amount of money gained
        """
        self.constructor.on_add_money(money)

    def on_pay_money(self, money):
        """
        Notifies the model and Map controller about bank account state change when user pays money.

        :param money:                   amount of money spent
        """
        self.constructor.on_pay_money(money)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
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

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
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

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
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

    def on_change_feature_unlocked_notification_state(self, notification_state):
        """
        Notifies the Constructor controller about feature unlocked notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.constructor.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        """
        Notifies the Constructor controller about construction completed notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.constructor.on_change_construction_completed_notification_state(notification_state)

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()