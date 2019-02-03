# ------------------- RSSIM_CORE MODULE -------------------
# __init__.py       implements functions to create all objects in the app.
# rssim_core.py     implements RSSim class - base class for game launch and main loop.
# ------------------- IMPORTS -------------------
from controller.app_controller import AppController
from controller.game_controller import GameController
from controller.map_controller import MapController
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
from car_skins import *
# ------------------- END IMPORTS -------------------


# ------------------- CONSTANTS -------------------
CURRENT_VERSION = (0, 9, 3)         # current app version
REQUIRED_TEXTURE_SIZE = 8192        # maximum texture resolution presented in the app
MIN_RESOLUTION_WIDTH = 1280         # minimum screen resolution width supported by the app UI
MIN_RESOLUTION_HEIGHT = 720         # minimum screen resolution height supported by the app UI
FPS_INTERVAL = 0.2                  # interval between FPS update
LOG_LEVEL_OFF = 30                  # integer log level high enough to cut off all logs
LOG_LEVEL_INFO = 20                 # integer log level which includes basic logs
LOG_LEVEL_DEBUG = 10                # integer log level which includes all possible logs
# ------------------- END CONSTANTS -------------------


# ------------------- FUNCTIONS -------------------
def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, loader):
    """
    Creates controller, model and view for App object.
    It is responsible for high-level properties, UI and events.
    Child objects:
        game                        Game object
        settings                    Settings object
        fps                         FPS object

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param loader:                  RSSim class pointer
    :return:                        App object controller
    """
    controller = AppController(loader)
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.game = _create_game(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                   batches, groups, controller)
    controller.settings = _create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                           batches, groups, controller)
    controller.fps = _create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                 batches, groups, controller)
    return controller


def _create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, app):
    """
    Creates controller, model and view for Game object.
    It is responsible for properties, UI and events related to the game process.
    Child objects:
        map                         Map object

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param app:                     App controller pointer
    :return:                        Game object controller
    """
    controller = GameController(app)
    app.game = controller
    model = GameModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = GameView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.map = _create_map(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                 batches, groups, controller)
    return controller


def _create_map(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, game):
    """
    Creates controller, model and view for Map object.
    It is responsible for properties, UI and events related to the map.
    Child objects:
        scheduler                   Scheduler object
        dispatcher                  Dispatcher object
        constructor                 Constructor object
        trains{}                    Train objects
        signals{}                   Signal objects
        train_routes{}              TrainRoute objects
        switches{}                  RailroadSwitch objects
        crossovers{}                Crossover objects

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param game:                    Game controller pointer
    :return:                        Map object controller
    """
    controller = MapController(game)
    game.map = controller
    controller.scheduler = _create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                             batches, groups, controller)
    controller.dispatcher = _create_dispatcher(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                               batches, groups, controller)
    controller.constructor = _create_constructor(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                                 batches, groups, controller)
    # read train IDs from database, create trains and append them to both dictionary and list
    user_db_cursor.execute('SELECT train_id FROM trains')
    train_ids = user_db_cursor.fetchall()
    if train_ids is not None:
        for i in train_ids:
            controller.trains[i[0]] = _create_train(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                                    batches, groups, controller, i[0])
            controller.trains_list.append(controller.trains[i[0]])
    # read signal tracks and base routes from database, create signals and append them to both dictionary and list
    config_db_cursor.execute('''SELECT DISTINCT track FROM signal_config''')
    signal_index = config_db_cursor.fetchall()
    for i in signal_index:
        controller.signals[i[0]] = {}

    config_db_cursor.execute('''SELECT track, base_route FROM signal_config''')
    signal_ids = config_db_cursor.fetchall()
    for i in signal_ids:
        controller.signals[i[0]][i[1]] \
            = _create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface,
                             batches, groups, controller, i[0], i[1])
        controller.signals_list.append(controller.signals[i[0]][i[1]])
    # read train route tracks and types from database, create train routes and append them to both dictionary and list
    config_db_cursor.execute('''SELECT DISTINCT track FROM train_route_config''')
    train_route_index = config_db_cursor.fetchall()
    for i in train_route_index:
        controller.train_routes[i[0]] = {}

    config_db_cursor.execute('''SELECT track, train_route FROM train_route_config''')
    train_route_ids = config_db_cursor.fetchall()
    for i in train_route_ids:
        controller.train_routes[i[0]][i[1]] \
            = _create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                  batches, groups, controller, i[0], i[1])
        controller.train_routes_sorted_list.append(controller.train_routes[i[0]][i[1]])
    # read switches tracks from database, create switches and append them to both dictionary and list
    user_db_cursor.execute('''SELECT DISTINCT track_param_1 FROM switches''')
    switch_track_param_1 = user_db_cursor.fetchall()
    for i in switch_track_param_1:
        controller.switches[i[0]] = {}

    user_db_cursor.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches''')
    switch_track_param_2 = user_db_cursor.fetchall()
    for i in switch_track_param_2:
        controller.switches[i[0]][i[1]] = {}

    user_db_cursor.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches''')
    switch_types = user_db_cursor.fetchall()
    for i in switch_types:
        controller.switches[i[0]][i[1]][i[2]] \
            = _create_railroad_switch(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                      batches, groups, controller, i[0], i[1], i[2])
        controller.switches_list.append(controller.switches[i[0]][i[1]][i[2]])
    # read crossovers tracks from database, create crossovers and append them to both dictionary and list
    user_db_cursor.execute('''SELECT DISTINCT track_param_1 FROM crossovers''')
    crossovers_track_param_1 = user_db_cursor.fetchall()
    for i in crossovers_track_param_1:
        controller.crossovers[i[0]] = {}

    user_db_cursor.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers''')
    crossovers_track_param_2 = user_db_cursor.fetchall()
    for i in crossovers_track_param_2:
        controller.crossovers[i[0]][i[1]] = {}

    user_db_cursor.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers''')
    crossovers_types = user_db_cursor.fetchall()
    for i in crossovers_types:
        controller.crossovers[i[0]][i[1]][i[2]] \
            = _create_crossover(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                batches, groups, controller, i[0], i[1], i[2])
        controller.crossovers_list.append(controller.crossovers[i[0]][i[1]][i[2]])

    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, app):
    """
    Creates controller, model and view for Settings object.
    It is responsible for user-defined settings.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param app:                     App controller pointer
    :return:                        Settings object controller
    """
    controller = SettingsController(app)
    app.settings = controller
    model = SettingsModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SettingsView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, app):
    """
    Creates controller, model and view for FPS object.
    It is responsible for real-time FPS calculation.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param app:                     App controller pointer
    :return:                        FPS object controller
    """
    controller = FPSController(app)
    app.fps = controller
    model = FPSModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = FPSView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, map_controller):
    """
    Creates controller, model and view for Scheduler object.
    It is responsible for properties, UI and events related to the train schedule.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :return:                        Scheduler object controller
    """
    controller = SchedulerController(map_controller)
    model = SchedulerModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SchedulerView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface,
                   batches, groups, map_controller, track, base_route):
    """
    Creates controller, model and view for Signal object.
    It is responsible for properties, UI and events related to the signal state.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :param track:                   signal track number
    :param base_route:              train route part which signal belongs to
    :return:                        Signal object controller
    """
    controller = SignalController(map_controller)
    controller.track = track
    controller.base_route = base_route
    model = SignalModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_signal_setup(track, base_route)
    view = SignalView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface,
                        batches, groups, map_controller, track, train_route):
    """
    Creates controller, model and view for TrainRoute object.
    It is responsible for properties, UI and events related to the train route.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :param track:                   train route track number
    :param train_route:             train route type
    :return:                        TrainRoute object controller
    """
    controller = TrainRouteController(map_controller)
    controller.track = track
    controller.train_route = train_route
    model = TrainRouteModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_train_route_setup(track, train_route)
    if model.opened:
        controller.parent_controller.on_set_trail_points(model.last_opened_by, model.trail_points_v2)

    view = TrainRouteView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_railroad_switch(user_db_connection, user_db_cursor, config_db_cursor, surface,
                            batches, groups, map_controller, track_param_1, track_param_2, switch_type):
    """
    Creates controller, model and view for RailroadSwitch object.
    It is responsible for properties, UI and events related to the railroad switch.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :param track_param_1:           straight track number
    :param track_param_2:           diverging track number
    :param switch_type:             switch location: left/right side of the map
    :return:                        RailroadSwitch object controller
    """
    controller = RailroadSwitchController(map_controller)
    controller.track_param_1 = track_param_1
    controller.track_param_2 = track_param_2
    controller.switch_type = switch_type
    model = RailroadSwitchModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_railroad_switch_setup(track_param_1, track_param_2, switch_type)
    view = RailroadSwitchView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_crossover(user_db_connection, user_db_cursor, config_db_cursor, surface,
                      batches, groups, map_controller, track_param_1, track_param_2, crossover_type):
    """
    Creates controller, model and view for Crossover object.
    It is responsible for properties, UI and events related to the crossover.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :param track_param_1:           first straight track number
    :param track_param_2:           second straight track number
    :param crossover_type:          crossover location: left/right side of the map
    :return:                        Crossover object controller
    """
    controller = CrossoverController(map_controller)
    controller.track_param_1 = track_param_1
    controller.track_param_2 = track_param_2
    controller.crossover_type = crossover_type
    model = CrossoverModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_crossover_setup(track_param_1, track_param_2, crossover_type)
    view = CrossoverView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_train(user_db_connection, user_db_cursor, config_db_cursor, surface,
                  batches, groups, map_controller, train_id):
    """
    Creates controller, model and view for Train object.
    It is responsible for properties, UI and events related to the train.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :param train_id:                train identification number
    :return:                        Train object controller
    """
    controller = TrainController(map_controller)
    controller.train_id = train_id
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_train_setup(train_id)
    view = TrainView(user_db_cursor, config_db_cursor, surface, batches, groups)
    view.car_head_image = CAR_HEAD_IMAGE
    view.car_mid_image = CAR_MID_IMAGE
    view.car_tail_image = CAR_TAIL_IMAGE
    view.boarding_light_image = BOARDING_LIGHT_IMAGE
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_dispatcher(user_db_connection, user_db_cursor, config_db_cursor, surface,
                       batches, groups, map_controller):
    """
    Creates controller, model and view for Dispatcher object.
    It is responsible for creating trains from schedule and assigning routes to approaching trains.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :return:                        Dispatcher object controller
    """
    controller = DispatcherController(map_controller)
    model = DispatcherModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = DispatcherView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def _create_constructor(user_db_connection, user_db_cursor, config_db_cursor, surface,
                        batches, groups, map_controller):
    """
    Creates controller, model and view for Constructor object.
    It is responsible for building new tracks and station environment.

    :param user_db_connection:      connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:          user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:        configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                 surface to draw all UI objects on
    :param batches:                 batches to group all labels and sprites
    :param groups:                  defines drawing layers (some labels and sprites behind others)
    :param map_controller:          Map controller pointer
    :return:                        Constructor object controller
    """
    controller = ConstructorController(map_controller)
    model = ConstructorModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = ConstructorView(user_db_cursor, config_db_cursor, surface, batches, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


# ------------------- END FUNCTIONS -------------------
