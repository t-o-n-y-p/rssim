from .controller_base import Controller


def _controller_is_active(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def _controller_is_not_active(fn):
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


class TrainRouteController(Controller):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller)
        self.track = None
        self.train_route = None

    def on_update_view(self):
        self.view.on_update()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    def on_save_state(self):
        self.model.on_save_state()

    def on_open_train_route(self):
        self.model.on_open_train_route()

    def on_close_train_route(self):
        self.model.on_open_train_route()

    def on_update_train_route_sections(self, last_car_position):
        self.model.on_update_train_route_sections(last_car_position)
