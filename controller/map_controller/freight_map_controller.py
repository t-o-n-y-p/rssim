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
        super().__init__(*self.create_map_elements(), map_id=FREIGHT_MAP, parent_controller=game_controller)

    def create_map_elements(self):
        view = FreightMapView(controller=self)
        model = FreightMapModel(controller=self, view=view)
        scheduler = FreightMapSchedulerController(self)
        constructor = FreightMapConstructorController(self)
        dispatcher = FreightMapDispatcherController(self)
        mini_map = FreightMiniMapController(self)
        narrator = FreightMapNarratorController(self)
        signals = {}
        signals_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config WHERE map_id = ?''', (FREIGHT_MAP, ))
        signal_index = CONFIG_DB_CURSOR.fetchall()
        for i in signal_index:
            signals[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config WHERE map_id = ?''', (FREIGHT_MAP, ))
        signal_ids = CONFIG_DB_CURSOR.fetchall()
        for i in signal_ids:
            signals[i[0]][i[1]] = FreightMapSignalController(self, *i)
            signals_list.append(signals[i[0]][i[1]])

        train_routes = {}
        train_routes_sorted_list = []
        CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM train_route_config WHERE map_id = ?''',
                                 (FREIGHT_MAP, ))
        train_route_index = CONFIG_DB_CURSOR.fetchall()
        for i in train_route_index:
            train_routes[i[0]] = {}

        CONFIG_DB_CURSOR.execute('''SELECT track, train_route FROM train_route_config WHERE map_id = ?''',
                                 (FREIGHT_MAP, ))
        train_route_ids = CONFIG_DB_CURSOR.fetchall()
        for i in train_route_ids:
            train_routes[i[0]][i[1]] = FreightTrainRouteController(self, *i)
            train_routes_sorted_list.append(train_routes[i[0]][i[1]])

        switches = {}
        switches_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches WHERE map_id = ?''', (FREIGHT_MAP, ))
        switch_track_param_1 = USER_DB_CURSOR.fetchall()
        for i in switch_track_param_1:
            switches[i[0]] = {}

        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches WHERE map_id = ?''',
                               (FREIGHT_MAP, ))
        switch_track_param_2 = USER_DB_CURSOR.fetchall()
        for i in switch_track_param_2:
            switches[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches WHERE map_id = ?''',
                               (FREIGHT_MAP, ))
        switch_types = USER_DB_CURSOR.fetchall()
        for i in switch_types:
            switches[i[0]][i[1]][i[2]] = FreightMapRailroadSwitchController(self, *i)
            switches_list.append(switches[i[0]][i[1]][i[2]])

        crossovers = {}
        crossovers_list = []
        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers WHERE map_id = ?''', (FREIGHT_MAP, ))
        crossovers_track_param_1 = USER_DB_CURSOR.fetchall()
        for i in crossovers_track_param_1:
            crossovers[i[0]] = {}

        USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers WHERE map_id = ?''',
                               (FREIGHT_MAP, ))
        crossovers_track_param_2 = USER_DB_CURSOR.fetchall()
        for i in crossovers_track_param_2:
            crossovers[i[0]][i[1]] = {}

        USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type 
                                  FROM crossovers WHERE map_id = ?''', (FREIGHT_MAP, ))
        crossovers_types = USER_DB_CURSOR.fetchall()
        for i in crossovers_types:
            crossovers[i[0]][i[1]][i[2]] = FreightMapCrossoverController(self, *i)
            crossovers_list.append(crossovers[i[0]][i[1]][i[2]])

        trains = {}
        trains_list = []
        USER_DB_CURSOR.execute('''SELECT train_id FROM trains WHERE map_id = ?''', (FREIGHT_MAP, ))
        train_ids = USER_DB_CURSOR.fetchall()
        if train_ids is not None:
            for i in train_ids:
                trains[i[0]] = FreightTrainController(self, i[0])
                trains_list.append(trains[i[0]])

        shops = []
        return model, view, scheduler, constructor, dispatcher, mini_map, narrator, signals, signals_list, \
            train_routes, train_routes_sorted_list, switches, switches_list, crossovers, crossovers_list, \
            trains, trains_list, shops
