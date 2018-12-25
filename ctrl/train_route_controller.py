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

    def on_open_train_route(self, train_id, cars):
        self.model.on_open_train_route(train_id, cars)

    def on_close_train_route(self):
        self.model.on_open_train_route()

    def on_update_train_route_sections(self, last_car_position):
        self.model.on_update_train_route_sections(last_car_position)

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    def on_update_priority(self, priority):
        self.model.on_update_priority(priority)

    def on_update_section_status(self, section, status):
        self.model.on_update_section_status(section, status)

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
