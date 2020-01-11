from typing import final

from controller.map_controller import MapController
from model.map_model.passenger_map_model import PassengerMapModel
from view.map_view.passenger_map_view import PassengerMapView
from controller.scheduler_controller.passenger_map_scheduler_controller import PassengerMapSchedulerController
from controller.constructor_controller.passenger_map_constructor_controller import PassengerMapConstructorController
from controller.dispatcher_controller.passenger_map_dispatcher_controller import PassengerMapDispatcherController
from controller.mini_map_controller.passenger_mini_map_controller import PassengerMiniMapController
from controller.signal_controller.passenger_map_signal_controller import PassengerMapSignalController
from controller.train_route_controller.passenger_train_route_controller import PassengerTrainRouteController
from controller.railroad_switch_controller.passenger_map_railroad_switch_controller \
    import PassengerMapRailroadSwitchController
from controller.crossover_controller.passenger_map_crossover_controller import PassengerMapCrossoverController
from controller.train_controller.passenger_train_controller import PassengerTrainController
from controller.shop_controller.passenger_map_shop_controller import PassengerMapShopController
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, PASSENGER_MAP


@final
class PassengerMapController(MapController):
    def __init__(self, game_controller):
        super().__init__(*self.create_map_elements(), map_id=PASSENGER_MAP, parent_controller=game_controller)

    def create_map_elements(self):
        view = PassengerMapView(controller=self)
        model = PassengerMapModel(controller=self, view=view)
        scheduler = PassengerMapSchedulerController(self)
        constructor = PassengerMapConstructorController(self)
        dispatcher = PassengerMapDispatcherController(self)
        mini_map = PassengerMiniMapController(self)
        signals = {}
        signals_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config WHERE map_id = ?''', (PASSENGER_MAP, ))
        signal_index = CONFIG_DB_CURSOR.fetchall()
        for i in signal_index:
            signals[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config WHERE map_id = ?''', (PASSENGER_MAP, ))
        signal_ids = CONFIG_DB_CURSOR.fetchall()
        for i in signal_ids:
            signals[i[0]][i[1]] = PassengerMapSignalController(self, *i)
            signals_list.append(signals[i[0]][i[1]])

        train_routes = {}
        train_routes_sorted_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM train_route_config WHERE map_id = ?''',
                                 (PASSENGER_MAP, ))
        train_route_index = CONFIG_DB_CURSOR.fetchall()
        for i in train_route_index:
            train_routes[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, train_route FROM train_route_config WHERE map_id = ?''',
                                 (PASSENGER_MAP, ))
        train_route_ids = CONFIG_DB_CURSOR.fetchall()
        for i in train_route_ids:
            train_routes[i[0]][i[1]] = PassengerTrainRouteController(self, *i)
            train_routes_sorted_list.append(train_routes[i[0]][i[1]])

        switches = {}
        switches_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches WHERE map_id = ?''', (PASSENGER_MAP, ))
        switch_track_param_1 = USER_DB_CURSOR.fetchall()
        for i in switch_track_param_1:
            switches[i[0]] = {}

        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches WHERE map_id = ?''',
                               (PASSENGER_MAP, ))
        switch_track_param_2 = USER_DB_CURSOR.fetchall()
        for i in switch_track_param_2:
            switches[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches WHERE map_id = ?''',
                               (PASSENGER_MAP, ))
        switch_types = USER_DB_CURSOR.fetchall()
        for i in switch_types:
            switches[i[0]][i[1]][i[2]] = PassengerMapRailroadSwitchController(self, *i)
            switches_list.append(switches[i[0]][i[1]][i[2]])

        crossovers = {}
        crossovers_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers WHERE map_id = ?''', (PASSENGER_MAP, ))
        crossovers_track_param_1 = USER_DB_CURSOR.fetchall()
        for i in crossovers_track_param_1:
            crossovers[i[0]] = {}

        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers WHERE map_id = ?''',
                               (PASSENGER_MAP, ))
        crossovers_track_param_2 = USER_DB_CURSOR.fetchall()
        for i in crossovers_track_param_2:
            crossovers[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type 
                                  FROM crossovers WHERE map_id = ?''', (PASSENGER_MAP, ))
        crossovers_types = USER_DB_CURSOR.fetchall()
        for i in crossovers_types:
            crossovers[i[0]][i[1]][i[2]] = PassengerMapCrossoverController(self, *i)
            crossovers_list.append(crossovers[i[0]][i[1]][i[2]])

        trains = {}
        trains_list = []
        USER_DB_CURSOR.execute('''SELECT train_id FROM trains WHERE map_id = ?''', (PASSENGER_MAP, ))
        train_ids = USER_DB_CURSOR.fetchall()
        if train_ids is not None:
            for i in train_ids:
                trains[i[0]] = PassengerTrainController(self, i[0])
                trains_list.append(trains[i[0]])

        shops = []
        CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = ?''', (PASSENGER_MAP, ))
        number_of_shops = CONFIG_DB_CURSOR.fetchone()[0]
        for i in range(number_of_shops):
            shops.append(PassengerMapShopController(self, i))

        return model, view, scheduler, constructor, dispatcher, mini_map, signals, signals_list, \
               train_routes, train_routes_sorted_list, switches, switches_list, crossovers, crossovers_list, \
               trains, trains_list, shops
