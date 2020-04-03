from typing import final

from controller.map_controller import MapController
from controller.narrator_controller.passenger_map_narrator_controller import PassengerMapNarratorController
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
        super().__init__(map_id=PASSENGER_MAP, parent_controller=game_controller)

    def create_view_and_model(self):
        view = PassengerMapView(controller=self)
        model = PassengerMapModel(controller=self, view=view)
        return view, model

    def create_scheduler(self):
        return PassengerMapSchedulerController(self)

    def create_constructor(self):
        return PassengerMapConstructorController(self)

    def create_dispatcher(self):
        return PassengerMapDispatcherController(self)

    def create_mini_map(self):
        return PassengerMiniMapController(self)

    def create_narrator(self):
        return PassengerMapNarratorController(self)

    def create_signals(self):
        signals = {}
        signals_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config WHERE map_id = ?''', (PASSENGER_MAP,))
        for i in CONFIG_DB_CURSOR.fetchall():
            signals[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config WHERE map_id = ?''', (PASSENGER_MAP,))
        for i in CONFIG_DB_CURSOR.fetchall():
            signals[i[0]][i[1]] = PassengerMapSignalController(self, *i)
            signals_list.append(signals[i[0]][i[1]])

        return signals, signals_list

    def create_train_routes(self):
        train_routes = {}
        train_routes_sorted_list = []
        CONFIG_DB_CURSOR.execute(
            '''SELECT DISTINCT track FROM train_route_config WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in CONFIG_DB_CURSOR.fetchall():
            train_routes[i[0]] = {}

        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route FROM train_route_config WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in CONFIG_DB_CURSOR.fetchall():
            train_routes[i[0]][i[1]] = PassengerTrainRouteController(self, *i)
            train_routes_sorted_list.append(train_routes[i[0]][i[1]])

        return train_routes, train_routes_sorted_list

    def create_switches(self):
        switches = {}
        switches_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches WHERE map_id = ?''', (PASSENGER_MAP,))
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT DISTINCT track_param_1, track_param_2 FROM switches WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT track_param_1, track_param_2, switch_type FROM switches WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]][i[1]][i[2]] = PassengerMapRailroadSwitchController(self, *i)
            switches_list.append(switches[i[0]][i[1]][i[2]])

        return switches, switches_list

    def create_crossovers(self):
        crossovers = {}
        crossovers_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers WHERE map_id = ?''', (PASSENGER_MAP,))
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT track_param_1, track_param_2, crossover_type FROM crossovers WHERE map_id = ?''', (PASSENGER_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]][i[1]][i[2]] = PassengerMapCrossoverController(self, *i)
            crossovers_list.append(crossovers[i[0]][i[1]][i[2]])

        return crossovers, crossovers_list

    def create_trains(self):
        trains = {}
        trains_list = []
        USER_DB_CURSOR.execute('''SELECT train_id FROM trains WHERE map_id = ?''', (PASSENGER_MAP,))
        try:
            for i in USER_DB_CURSOR.fetchall():
                trains[i[0]] = PassengerTrainController(self, i[0])
                trains_list.append(trains[i[0]])
        except TypeError:
            pass

        return trains, trains_list

    def create_shops(self):
        shops = []
        CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = ?''', (PASSENGER_MAP,))
        for i in range(CONFIG_DB_CURSOR.fetchone()[0]):
            shops.append(PassengerMapShopController(self, i))

        return shops
