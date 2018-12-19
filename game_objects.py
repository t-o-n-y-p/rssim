from ctrl import AppController, GameController, MapController, SettingsController, FPSController, SchedulerController, \
    SignalController
from model import AppModel, GameModel, MapModel, SettingsModel, FPSModel, SchedulerModel, SignalModel
from view import AppView, GameView, MapView, SettingsView, FPSView, SchedulerView, SignalView


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
    controller.signals[0]['right_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        0, 'right_entry_base_route')
    for i in range(1, 33):
        controller.signals[i] = {}
        controller.signals[i]['left_exit_platform_base_route'] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                            i, 'left_exit_platform_base_route')
        controller.signals[i]['right_exit_platform_base_route'] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                            i, 'right_exit_platform_base_route')

    controller.signals[100] = {}
    controller.signals[100]['left_side_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        100, 'left_side_entry_base_route')
    controller.signals[100]['right_side_entry_base_route'] \
        = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, controller,
                        100, 'right_side_entry_base_route')
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
    model = SignalModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SignalView(surface, batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.track = track
    controller.base_route = base_route
    return controller
