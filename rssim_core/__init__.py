from controller.app_controller import AppController
from controller.game_controller import GameController
from controller.map_controller.passenger_map_controller import PassengerMapController
from controller.settings_controller import SettingsController
from controller.fps_controller import FPSController
from controller.scheduler_controller import SchedulerController
from controller.signal_controller import SignalController
from controller.train_route_controller import TrainRouteController
from controller.railroad_switch_controller import RailroadSwitchController
from controller.crossover_controller import CrossoverController
from controller.train_controller import TrainController
from controller.dispatcher_controller import DispatcherController
from controller.constructor_controller import ConstructorController
from model.app_model import AppModel
from model.game_model import GameModel
from model.map_model import MapModel
from model.settings_model import SettingsModel
from model.fps_model import FPSModel
from model.scheduler_model import SchedulerModel
from model.signal_model import SignalModel
from model.train_route_model import TrainRouteModel
from model.railroad_switch_model import RailroadSwitchModel
from model.crossover_model import CrossoverModel
from model.train_model import TrainModel
from model.dispatcher_model import DispatcherModel
from model.constructor_model import ConstructorModel
from view.app_view import AppView
from view.game_view import GameView
from view.map_view import MapView
from view.settings_view import SettingsView
from view.fps_view import FPSView
from view.scheduler_view import SchedulerView
from view.signal_view import SignalView
from view.train_route_view import TrainRouteView
from view.railroad_switch_view import RailroadSwitchView
from view.crossover_view import CrossoverView
from view.train_view import TrainView
from view.dispatcher_view import DispatcherView
from view.constructor_view import ConstructorView
from textures import *
from database import CONFIG_DB_CURSOR, USER_DB_CURSOR


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION = (0, 9, 5)         # current app version
REQUIRED_TEXTURE_SIZE = 8192        # maximum texture resolution presented in the app
FPS_INTERVAL = 0.2                  # interval between FPS update
LOG_LEVEL_OFF = 30                  # integer log level high enough to cut off all logs
LOG_LEVEL_INFO = 20                 # integer log level which includes basic logs
LOG_LEVEL_DEBUG = 10                # integer log level which includes all possible logs
# ------------------- END CONSTANTS -------------------


def create_app(loader):
    """
    Creates controller, model and view for App object.
    It is responsible for high-level properties, UI and events.
    Child objects:
        game                        Game object
        settings                    Settings object
        fps                         FPS object

    :param loader:                  RSSim class pointer
    :return:                        App object controller
    """
    controller = AppController(loader)
    model = AppModel()
    view = AppView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.game = _create_game(controller)
    controller.settings = _create_settings(controller)
    controller.fps = _create_fps(controller)
    return controller


def _create_game(app):
    """
    Creates controller, model and view for Game object.
    It is responsible for properties, UI and events related to the game process.
    Child objects:
        map                         Map object

    :param app:                     App controller pointer
    :return:                        Game object controller
    """
    controller = GameController(app)
    model = GameModel()
    view = GameView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.maps.append(_create_passenger_map(controller))
    return controller


def _create_passenger_map(game):
    """
    Creates controller, model and view for Map object.
    It is responsible for properties, UI and events related to the map.
    Child objects:
        scheduler                   Scheduler object
        dispatcher                  Dispatcher object
        constructor                 Constructor object
        trains                      Train objects
        signals                     Signal objects
        train_routes                TrainRoute objects
        switches                    RailroadSwitch objects
        crossovers                  Crossover objects

    :param game:                    Game controller pointer
    :return:                        Map object controller
    """
    controller = PassengerMapController(game)
    controller.scheduler = _create_scheduler(controller)
    controller.dispatcher = _create_dispatcher(controller)
    controller.constructor = _create_constructor(controller)
    # read train IDs from database, create trains and append them to both dictionary and list
    USER_DB_CURSOR.execute('SELECT train_id FROM trains')
    train_ids = USER_DB_CURSOR.fetchall()
    if train_ids is not None:
        for i in train_ids:
            controller.trains[i[0]] = _create_train(controller, i[0])
            controller.trains_list.append(controller.trains[i[0]])
    # read signal tracks and base routes from database, create signals and append them to both dictionary and list
    CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config''')
    signal_index = CONFIG_DB_CURSOR.fetchall()
    for i in signal_index:
        controller.signals[i[0]] = {}

    CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config''')
    signal_ids = CONFIG_DB_CURSOR.fetchall()
    for i in signal_ids:
        controller.signals[i[0]][i[1]] \
            = _create_signal(controller, i[0], i[1])
        controller.signals_list.append(controller.signals[i[0]][i[1]])
    # read train route tracks and types from database, create train routes and append them to both dictionary and list
    CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM train_route_config''')
    train_route_index = CONFIG_DB_CURSOR.fetchall()
    for i in train_route_index:
        controller.train_routes[i[0]] = {}

    CONFIG_DB_CURSOR.execute('''SELECT track, train_route FROM train_route_config''')
    train_route_ids = CONFIG_DB_CURSOR.fetchall()
    for i in train_route_ids:
        controller.train_routes[i[0]][i[1]] \
            = _create_train_route(controller, i[0], i[1])
        controller.train_routes_sorted_list.append(controller.train_routes[i[0]][i[1]])
    # read switches tracks from database, create switches and append them to both dictionary and list
    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches''')
    switch_track_param_1 = USER_DB_CURSOR.fetchall()
    for i in switch_track_param_1:
        controller.switches[i[0]] = {}

    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches''')
    switch_track_param_2 = USER_DB_CURSOR.fetchall()
    for i in switch_track_param_2:
        controller.switches[i[0]][i[1]] = {}

    USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches''')
    switch_types = USER_DB_CURSOR.fetchall()
    for i in switch_types:
        controller.switches[i[0]][i[1]][i[2]] \
            = _create_railroad_switch(controller, i[0], i[1], i[2])
        controller.switches_list.append(controller.switches[i[0]][i[1]][i[2]])
    # read crossovers tracks from database, create crossovers and append them to both dictionary and list
    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers''')
    crossovers_track_param_1 = USER_DB_CURSOR.fetchall()
    for i in crossovers_track_param_1:
        controller.crossovers[i[0]] = {}

    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers''')
    crossovers_track_param_2 = USER_DB_CURSOR.fetchall()
    for i in crossovers_track_param_2:
        controller.crossovers[i[0]][i[1]] = {}

    USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers''')
    crossovers_types = USER_DB_CURSOR.fetchall()
    for i in crossovers_types:
        controller.crossovers[i[0]][i[1]][i[2]] \
            = _create_crossover(controller, i[0], i[1], i[2])
        controller.crossovers_list.append(controller.crossovers[i[0]][i[1]][i[2]])

    model = MapModel()
    view = MapView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_settings(app):
    """
    Creates controller, model and view for Settings object.
    It is responsible for user-defined settings.

    :param app:                     App controller pointer
    :return:                        Settings object controller
    """
    controller = SettingsController(app)
    model = SettingsModel()
    view = SettingsView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_fps(app):
    """
    Creates controller, model and view for FPS object.
    It is responsible for real-time FPS calculation.

    :param app:                     App controller pointer
    :return:                        FPS object controller
    """
    controller = FPSController(app)
    model = FPSModel()
    view = FPSView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_scheduler(map_controller):
    """
    Creates controller, model and view for Scheduler object.
    It is responsible for properties, UI and events related to the train schedule.

    :param map_controller:          Map controller pointer
    :return:                        Scheduler object controller
    """
    controller = SchedulerController(map_controller)
    model = SchedulerModel()
    view = SchedulerView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_signal(map_controller, track, base_route):
    """
    Creates controller, model and view for Signal object.
    It is responsible for properties, UI and events related to the signal state.

    :param map_controller:          Map controller pointer
    :param track:                   signal track number
    :param base_route:              base route (train route part) which signal belongs to
    :return:                        Signal object controller
    """
    controller = SignalController(map_controller, track, base_route)
    model = SignalModel(track, base_route)
    view = SignalView(track, base_route, RED_SIGNAL_IMAGE, GREEN_SIGNAL_IMAGE)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_train_route(map_controller, track, train_route):
    """
    Creates controller, model and view for TrainRoute object.
    It is responsible for properties, UI and events related to the train route.

    :param map_controller:          Map controller pointer
    :param track:                   train route track number
    :param train_route:             train route type
    :return:                        TrainRoute object controller
    """
    controller = TrainRouteController(map_controller, track, train_route)
    model = TrainRouteModel(track, train_route)
    if model.opened:
        controller.parent_controller.on_set_trail_points(model.last_opened_by, model.trail_points_v2)

    view = TrainRouteView(track, train_route)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_railroad_switch(map_controller, track_param_1, track_param_2, switch_type):
    """
    Creates controller, model and view for RailroadSwitch object.
    It is responsible for properties, UI and events related to the railroad switch.

    :param map_controller:          Map controller pointer
    :param track_param_1:           straight track number
    :param track_param_2:           diverging track number
    :param switch_type:             switch location: left/right side of the map
    :return:                        RailroadSwitch object controller
    """
    controller = RailroadSwitchController(map_controller, track_param_1, track_param_2, switch_type)
    model = RailroadSwitchModel(track_param_1, track_param_2, switch_type)
    view = RailroadSwitchView(track_param_1, track_param_2, switch_type)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_crossover(map_controller, track_param_1, track_param_2, crossover_type):
    """
    Creates controller, model and view for Crossover object.
    It is responsible for properties, UI and events related to the crossover.

    :param map_controller:          Map controller pointer
    :param track_param_1:           first straight track number
    :param track_param_2:           second straight track number
    :param crossover_type:          crossover location: left/right side of the map
    :return:                        Crossover object controller
    """
    controller = CrossoverController(map_controller, track_param_1, track_param_2, crossover_type)
    model = CrossoverModel(track_param_1, track_param_2, crossover_type)
    view = CrossoverView(track_param_1, track_param_2, crossover_type)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_train(map_controller, train_id):
    """
    Creates controller, model and view for Train object from the database.
    It is responsible for properties, UI and events related to the train.

    :param map_controller:          Map controller pointer
    :param train_id:                train identification number
    :return:                        Train object controller
    """
    controller = TrainController(map_controller, train_id)
    model = TrainModel(train_id)
    model.on_train_setup(train_id)
    view = TrainView(train_id, CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_dispatcher(map_controller):
    """
    Creates controller, model and view for Dispatcher object.
    It is responsible for assigning routes to approaching trains.

    :param map_controller:          Map controller pointer
    :return:                        Dispatcher object controller
    """
    controller = DispatcherController(map_controller)
    model = DispatcherModel()
    view = DispatcherView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_constructor(map_controller):
    """
    Creates controller, model and view for Constructor object.
    It is responsible for building new tracks and station environment.

    :param map_controller:          Map controller pointer
    :return:                        Constructor object controller
    """
    controller = ConstructorController(map_controller)
    model = ConstructorModel()
    view = ConstructorView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller
