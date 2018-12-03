from ctrl import AppController, GameController, MapController
from model import AppModel, GameModel, MapModel
from view import AppView, GameView, MapView


def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller


def create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, parent_controller):
    controller = GameController(parent_controller)
    parent_controller.init_controllers.append(controller)
    parent_controller.child_controllers.append(controller)
    parent_controller.exclusive_child_controllers.append(controller)
    model = GameModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = GameView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller


def create_map(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, parent_controller):
    controller = MapController(parent_controller)
    parent_controller.init_controllers.append(controller)
    parent_controller.child_controllers.append(controller)
    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller
