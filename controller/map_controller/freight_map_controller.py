from typing import final

from controller.map_controller import MapController
from controller.narrator_controller.freight_map_narrator_controller import FreightMapNarratorController
from model.map_model.freight_map_model import FreightMapModel
from view.map_view.freight_map_view import FreightMapView
from controller.scheduler_controller.freight_map_scheduler_controller import FreightMapSchedulerController
from controller.constructor_controller.freight_map_constructor_controller import FreightMapConstructorController
from controller.dispatcher_controller.freight_map_dispatcher_controller import FreightMapDispatcherController
from controller.mini_map_controller.freight_mini_map_controller import FreightMiniMapController
from controller.signal_controller.freight_map_signal_controller import FreightMapSignalController
from controller.train_route_controller.freight_train_route_controller import FreightTrainRouteController
from controller.railroad_switch_controller.freight_map_railroad_switch_controller \
    import FreightMapRailroadSwitchController
from controller.crossover_controller.freight_map_crossover_controller import FreightMapCrossoverController
from controller.train_controller.freight_train_controller import FreightTrainController
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, FREIGHT_MAP


@final
class FreightMapController(MapController):
    def __init__(self, game_controller):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=game_controller)

    def create_view_and_model(self):
        view = FreightMapView(controller=self)
        model = FreightMapModel(controller=self, view=view)
        return view, model

    def create_scheduler(self):
        return FreightMapSchedulerController(self)

    def create_constructor(self):
        return FreightMapConstructorController(self)

    def create_dispatcher(self):
        return FreightMapDispatcherController(self)

    def create_mini_map(self):
        return FreightMiniMapController(self)

    def create_narrator(self):
        return FreightMapNarratorController(self)

    def create_signals(self):
        signals = {}
        signals_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config WHERE map_id = ?''', (FREIGHT_MAP,))
        for i in CONFIG_DB_CURSOR.fetchall():
            signals[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config WHERE map_id = ?''', (FREIGHT_MAP,))
        for i in CONFIG_DB_CURSOR.fetchall():
            signals[i[0]][i[1]] = FreightMapSignalController(self, *i)
            signals_list.append(signals[i[0]][i[1]])

        return signals, signals_list

    def create_train_routes(self):
        train_routes = {}
        train_routes_sorted_list = []
        CONFIG_DB_CURSOR.execute(
            '''SELECT DISTINCT track FROM train_route_config WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in CONFIG_DB_CURSOR.fetchall():
            train_routes[i[0]] = {}

        CONFIG_DB_CURSOR.execute(
            '''SELECT track, train_route FROM train_route_config WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in CONFIG_DB_CURSOR.fetchall():
            train_routes[i[0]][i[1]] = FreightTrainRouteController(self, *i)
            train_routes_sorted_list.append(train_routes[i[0]][i[1]])

        return train_routes, train_routes_sorted_list

    def create_switches(self):
        switches = {}
        switches_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches WHERE map_id = ?''', (FREIGHT_MAP,))
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT DISTINCT track_param_1, track_param_2 FROM switches WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT track_param_1, track_param_2, switch_type FROM switches WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            switches[i[0]][i[1]][i[2]] = FreightMapRailroadSwitchController(self, *i)
            switches_list.append(switches[i[0]][i[1]][i[2]])

        return switches, switches_list

    def create_crossovers(self):
        crossovers = {}
        crossovers_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers WHERE map_id = ?''', (FREIGHT_MAP,))
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute(
            '''SELECT track_param_1, track_param_2, crossover_type FROM crossovers WHERE map_id = ?''', (FREIGHT_MAP,)
        )
        for i in USER_DB_CURSOR.fetchall():
            crossovers[i[0]][i[1]][i[2]] = FreightMapCrossoverController(self, *i)
            crossovers_list.append(crossovers[i[0]][i[1]][i[2]])

        return crossovers, crossovers_list

    def create_trains(self):
        trains = {}
        trains_list = []
        USER_DB_CURSOR.execute('''SELECT train_id FROM trains WHERE map_id = ?''', (FREIGHT_MAP,))
        try:
            for i in USER_DB_CURSOR.fetchall():
                trains[i[0]] = FreightTrainController(self, i[0])
                trains_list.append(trains[i[0]])
        except TypeError:
            pass

        return trains, trains_list

    def create_shops(self):
        return []
