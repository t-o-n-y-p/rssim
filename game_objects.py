from ctrl import AppController, GameController, MapController, SettingsController, FPSController, SchedulerController, \
                 SignalController, TrainRouteController, RailroadSwitchController
from model import AppModel, GameModel, MapModel, SettingsModel, FPSModel, SchedulerModel, SignalModel, TrainRouteModel,\
                  RailroadSwitchModel
from view import AppView, GameView, MapView, SettingsView, FPSView, SchedulerView, SignalView, TrainRouteView, \
                 RailroadSwitchView


def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.game = create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                  controller)
    controller.settings = create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                          controller)
    controller.fps = create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                controller)
    return controller


def create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, app):
    controller = GameController(app)
    app.game = controller
    model = GameModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = GameView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.map = create_map(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                controller)
    return controller


def create_map(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, game):
    controller = MapController(game)
    game.map = controller
    controller.scheduler = create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                            batch, groups, controller)
    config_db_cursor.execute('''SELECT DISTINCT track FROM signal_config''')
    signal_index = config_db_cursor.fetchall()
    for i in signal_index:
        controller.signals[i[0]] = {}

    config_db_cursor.execute('''SELECT track, base_route FROM signal_config''')
    signal_ids = config_db_cursor.fetchall()
    for i in signal_ids:
        controller.signals[i[0]][i[1]] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                            controller, i[0], i[1])
        controller.signals_list.append(controller.signals[i[0]][i[1]])

    config_db_cursor.execute('''SELECT DISTINCT track FROM train_route_config''')
    train_route_index = config_db_cursor.fetchall()
    for i in train_route_index:
        controller.train_routes[i[0]] = {}

    config_db_cursor.execute('''SELECT track, train_route FROM train_route_config''')
    train_route_ids = config_db_cursor.fetchall()
    for i in train_route_ids:
        controller.train_routes[i[0]][i[1]] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i[0], i[1])
        controller.train_routes_sorted_list.append(controller.train_routes[i[0]][i[1]])

    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, app):
    controller = SettingsController(app)
    app.settings = controller
    model = SettingsModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SettingsView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, app):
    controller = FPSController(app)
    app.fps = controller
    model = FPSModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = FPSView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, map_controller):
    controller = SchedulerController(map_controller)
    map_controller.scheduler = controller
    model = SchedulerModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SchedulerView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, map_controller,
                  track, base_route):
    controller = SignalController(map_controller)
    controller.track = track
    controller.base_route = base_route
    model = SignalModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_signal_setup(track, base_route)
    view = SignalView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, map_controller,
                       track, train_route):
    controller = TrainRouteController(map_controller)
    controller.track = track
    controller.train_route = train_route
    model = TrainRouteModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_train_route_setup(track, train_route)
    view = TrainRouteView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_railroad_switch(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, map_controller,
                           track_param_1, track_param_2, switch_type):
    controller = RailroadSwitchController(map_controller)
    controller.track_param_1 = track_param_1
    controller.track_param_2 = track_param_2
    controller.switch_type = switch_type
    model = RailroadSwitchModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_railroad_switch_setup(track_param_1, track_param_2, switch_type)
    view = RailroadSwitchView(user_db_cursor, config_db_cursor, surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller
