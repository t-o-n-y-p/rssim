from ctrl import AppController, GameController, MapController, SettingsController, FPSController, SchedulerController, \
                 SignalController, TrainRouteController, RailroadSwitchController
from model import AppModel, GameModel, MapModel, SettingsModel, FPSModel, SchedulerModel, SignalModel, TrainRouteModel,\
                  RailroadSwitchModel
from view import AppView, GameView, MapView, SettingsView, FPSView, SchedulerView, SignalView, TrainRouteView, \
                 RailroadSwitchView


def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(surface, batch, groups)
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
    view = GameView(surface, batch, groups)
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
    controller.signals[0] = {}
    controller.signals[0]['left_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        0, 'left_entry_base_route')
    controller.signals_list.append(controller.signals[0]['left_entry_base_route'])
    controller.signals[0]['right_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        0, 'right_entry_base_route')
    controller.signals_list.append(controller.signals[0]['right_entry_base_route'])
    for i in range(1, 33):
        controller.signals[i] = {}
        controller.train_routes[i] = {}
        controller.signals[i]['left_exit_platform_base_route'] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                            i, 'left_exit_platform_base_route')
        controller.signals_list.append(controller.signals[i]['left_exit_platform_base_route'])
        controller.signals[i]['right_exit_platform_base_route'] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                            i, 'right_exit_platform_base_route')
        controller.signals_list.append(controller.signals[i]['right_exit_platform_base_route'])

    controller.signals[100] = {}
    controller.signals[100]['left_side_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        100, 'left_side_entry_base_route')
    controller.signals_list.append(controller.signals[100]['left_side_entry_base_route'])
    controller.signals[100]['right_side_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        100, 'right_side_entry_base_route')
    controller.signals_list.append(controller.signals[100]['right_side_entry_base_route'])
    controller.train_routes[0] = {}
    controller.train_routes[0]['left_approaching'] \
        = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                             0, 'left_approaching')
    controller.train_routes_sorted_list.append(controller.train_routes[0]['left_approaching'])
    controller.train_routes[0]['right_approaching'] \
        = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                             0, 'right_approaching')
    controller.train_routes_sorted_list.append(controller.train_routes[0]['right_approaching'])
    for i in range(1, 25):
        controller.train_routes[i]['left_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_entry'])
        controller.train_routes[i]['right_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_entry'])
        controller.train_routes[i]['left_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_exit'])
        controller.train_routes[i]['right_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_exit'])

    for i in range(21, 32, 2):
        controller.train_routes[i]['left_side_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_side_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_side_entry'])
        controller.train_routes[i]['left_side_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_side_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_side_exit'])

    for i in range(22, 33, 2):
        controller.train_routes[i]['right_side_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_side_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_side_entry'])
        controller.train_routes[i]['right_side_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_side_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_side_exit'])

    for i in range(25, 32, 2):
        controller.train_routes[i]['right_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_entry'])
        controller.train_routes[i]['right_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'right_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['right_exit'])

    for i in range(26, 33, 2):
        controller.train_routes[i]['left_entry'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_entry')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_entry'])
        controller.train_routes[i]['left_exit'] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups,
                                 controller, i, 'left_exit')
        controller.train_routes_sorted_list.append(controller.train_routes[i]['left_exit'])

    controller.train_routes[100] = {}
    controller.train_routes[100]['left_side_approaching'] \
        = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                             100, 'left_side_approaching')
    controller.train_routes_sorted_list.append(controller.train_routes[100]['left_side_approaching'])
    controller.train_routes[100]['right_side_approaching'] \
        = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                             100, 'right_side_approaching')
    controller.train_routes_sorted_list.append(controller.train_routes[100]['right_side_approaching'])
    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(surface, batch, groups)
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
    view = SettingsView(surface, batch, groups)
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
    view = FPSView(surface, batch, groups)
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
    view = SchedulerView(surface, batch, groups)
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
    view = SignalView(surface, batch, groups)
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
    view = TrainRouteView(surface, batch, groups)
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
    view = RailroadSwitchView(surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller
