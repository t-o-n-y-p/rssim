from ctrl import AppController
from model import AppModel
from view import AppView


def create_app(user_db_connection, surface, batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection)
    view = AppView(surface, batch, groups)
    controller.model = model
    controller.view = view
    view.on_assign_controller(controller)
    model.on_assign_view(view)
    if controller.to_be_activated_during_startup:
        controller.on_activate()

    return controller
