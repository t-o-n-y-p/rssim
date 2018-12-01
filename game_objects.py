from ctrl import AppController
from model import AppModel
from view import AppView


def create_app(game_config, surface, batch, groups):
    controller = AppController()
    model = AppModel(game_config)
    view = AppView(game_config, surface, batch, groups)
    controller.model = model
    controller.view = view
    controller.on_activate()
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    return controller
