from ctrl import AppController, GameController, MapController, SettingsController, FPSController, SchedulerController
from model import AppModel, GameModel, MapModel, SettingsModel, FPSModel, SchedulerModel
from view import AppView, GameView, MapView, SettingsView, FPSView, SchedulerView


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
