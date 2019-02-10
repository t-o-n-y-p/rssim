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
        self.logger.info('START INIT')
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
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view and all child views to update fade-in/fade-out animations
        and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.logger.info('START ON_UPDATE_VIEW')
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

        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Map object: controller and model. Model activates the view if necessary.
        Also activates all child objects.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
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

        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
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

        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.
        Note that adjusting base offset is made by on_change_base_offset handler,
        which is called after screen resolution is updated.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
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
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_change_base_offset(self, new_base_offset):
        """
        Notifies the view and all child controllers about base offset update.

        :param new_base_offset:         new base offset
        """
        self.logger.info('START ON_CHANGE_BASE_OFFSET')
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

        self.logger.info('END ON_CHANGE_BASE_OFFSET')

    def on_unlock_track(self, track):
        """
        Notifies the model, the Scheduler, Dispatcher controllers
        and the corresponding Signal controllers the track is unlocked.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK')
        self.model.on_unlock_track(track)
        self.scheduler.on_unlock_track(track)
        self.dispatcher.on_unlock_track(track)
        for i in self.signals[track]:
            self.signals[track][i].on_unlock()

        # when left or right side entry becomes available, unlock corresponding side entry signal
        self.logger.debug(f'track: {track}')
        if track == LEFT_SIDE_ENTRY_FIRST_TRACK:
            self.signals[SIDE_ENTRY_EXIT_MASK]['left_side_entry_base_route'].on_unlock()
            self.logger.debug('left side entry signal unlocked')

        if track == RIGHT_SIDE_ENTRY_FIRST_TRACK:
            self.signals[SIDE_ENTRY_EXIT_MASK]['right_side_entry_base_route'].on_unlock()
            self.logger.debug('right side entry signal unlocked')

        self.logger.info('END ON_UNLOCK_TRACK')

    def on_activate_view(self):
        """
        Activates the view and all Signal, Train route, Railroad switch, Crossover, Train views
        if user opened game screen in the app.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
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

        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_deactivate_view(self):
        """
        Deactivates the view and all child views if user either closed game screen or opened settings screen.
        """
        self.logger.info('START ON_DEACTIVATE_VIEW')
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

        self.logger.info('END ON_DEACTIVATE_VIEW')

    def on_zoom_in(self):
        """
        Notifies the view and all Signal, Train route, Railroad switch, Crossover, Train views to zoom in all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler
        which is called after scale factor is updated.
        """
        self.logger.info('START ON_ZOOM_IN')
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
        self.logger.info('END ON_ZOOM_IN')

    def on_zoom_out(self):
        """
        Notifies the view and all Signal, Train route, Railroad switch, Crossover, Train views to zoom out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler
        which is called after scale factor is updated.
        """
        self.logger.info('START ON_ZOOM_OUT')
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
        self.logger.info('END ON_ZOOM_OUT')

    def on_save_state(self):
        """
        Notifies the model and all child controllers to save state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
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

        self.logger.info('END ON_SAVE_STATE')

    def on_update_time(self, game_time):
        """
        Notifies all Train route controllers sorted by priority, Train controllers,
        Scheduler, Dispatcher, Constructor controllers about in-game time update.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
        # train routes are sorted by priority to implement some kind of queue
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        self.logger.debug('train routes are sorted successfully')
        for route in self.train_routes_sorted_list:
            route.on_update_time(game_time)

        # since dictionary items cannot be removed right inside "for" statement,
        # collect trains which has departed successfully and should be removed from the game
        successful_departure_state = []
        for train in self.trains_list:
            train.on_update_time(game_time)
            if train.model.state == 'successful_departure':
                self.logger.debug(f'successful_departure state detected for train {train.train_id}')
                successful_departure_state.append(train.train_id)

        self.logger.debug(f'trains in successful_departure state: {successful_departure_state}')
        self.logger.debug(f'trains in operation: {list(self.trains.keys())}')
        self.logger.debug(f'trains list length: {len(self.trains_list)}')
        for train_id in successful_departure_state:
            self.trains[train_id].on_deactivate()
            self.trains_list.remove(self.trains.pop(train_id))
            self.logger.debug(f'trains in operation: {list(self.trains.keys())}')
            self.logger.debug(f'trains list length: {len(self.trains_list)}')

        self.scheduler.on_update_time(game_time)
        self.dispatcher.on_update_time(game_time)
        self.constructor.on_update_time(game_time)
        self.logger.info('END ON_UPDATE_TIME')

    def on_level_up(self, level):
        """
        Notifies the model, the Scheduler and Constructor controllers about level update.

        :param level:                   new level value
        """
        self.logger.info('START ON_LEVEL_UP')
        self.scheduler.on_level_up(level)
        self.constructor.on_level_up(level)
        self.logger.info('END ON_LEVEL_UP')

    def on_open_schedule(self):
        """
        Activates Scheduler view to open Scheduler screen for player.
        """
        self.logger.info('START ON_OPEN_SCHEDULE')
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
        self.logger.info('END ON_OPEN_SCHEDULE')

    def on_open_constructor(self):
        """
        Activates Constructor view to open Scheduler screen for player.
        """
        self.logger.info('START ON_OPEN_CONSTRUCTOR')
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
        self.logger.info('END ON_OPEN_CONSTRUCTOR')

    @map_view_is_active
    def on_close_schedule(self):
        """
        Activates back all buttons which are hidden when Scheduler view is active:
        zoom in/out buttons and open schedule button.
        """
        self.logger.info('START ON_CLOSE_SCHEDULE')
        self.view.on_activate_zoom_buttons()
        self.view.open_schedule_button.on_activate()
        self.logger.info('END ON_CLOSE_SCHEDULE')

    @map_view_is_active
    def on_close_constructor(self):
        """
        Activates back all buttons which are hidden when Constructor view is active:
        zoom in/out buttons and open constructor button.
        """
        self.logger.info('START ON_CLOSE_CONSTRUCTOR')
        self.view.on_activate_zoom_buttons()
        self.view.open_constructor_button.on_activate()
        self.logger.info('END ON_CLOSE_CONSTRUCTOR')

    def on_switch_signal_to_green(self, signal_track, signal_base_route):
        """
        Notifies particular Signal controller about state change to green.

        :param signal_track:                    signal track code from base route system
        :param signal_base_route:               signal base route type
        """
        self.logger.info('START ON_SWITCH_SIGNAL_TO_GREEN')
        self.signals[signal_track][signal_base_route].on_switch_to_green()
        self.logger.info('END ON_SWITCH_SIGNAL_TO_GREEN')

    def on_switch_signal_to_red(self, signal_track, signal_base_route):
        """
        Notifies particular Signal controller about state change to red.

        :param signal_track:                    signal track code from base route system
        :param signal_base_route:               signal base route type
        """
        self.logger.info('START ON_SWITCH_SIGNAL_TO_RED')
        self.signals[signal_track][signal_base_route].on_switch_to_red()
        self.logger.info('END ON_SWITCH_SIGNAL_TO_RED')

    def on_update_train_route_sections(self, track, train_route, last_car_position):
        self.train_routes[track][train_route].on_update_train_route_sections(last_car_position)

    def on_update_train_route_section_status(self, train_route_data, status):
        self.train_routes[
            train_route_data[TRAIN_ROUTE_DATA_TRACK_NUMBER]
        ][
            train_route_data[TRAIN_ROUTE_DATA_TYPE]
        ].on_update_section_status(train_route_data[TRAIN_ROUTE_DATA_SECTION_NUMBER], status)

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
        self.trains_list.append(train)
        self.dispatcher.on_add_train(train)
        train.parent_controller.on_open_train_route(track, train_route, train_id, cars)
        train.on_activate()
        if not self.view.is_activated:
            train.on_deactivate_view()

    def on_add_money(self, money):
        self.constructor.on_add_money(money)

    def on_pay_money(self, money):
        self.constructor.on_pay_money(money)

    def on_add_car_collection(self, car_collection_id):
        self.model.on_add_car_collection(car_collection_id)
