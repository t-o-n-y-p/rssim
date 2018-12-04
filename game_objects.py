from ctrl import AppController, GameController, MapController, SettingsController
from model import AppModel, GameModel, MapModel, SettingsModel
from view import AppView, GameView, MapView, SettingsView


def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller


def create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, app):
    controller = GameController(app)
    app.game = controller
    model = GameModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = GameView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller


def create_map(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, game):
    controller = MapController(game)
    game.map = controller
    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller


def create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, app):
    controller = SettingsController(app)
    app.settings = controller
    model = SettingsModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SettingsView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller
