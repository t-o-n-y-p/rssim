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


def _signal_belongs_to_track(fn):
    def _unlock_signal_if_belongs_to_track(*args, **kwargs):
        if args[1] == args[0].track:
            fn(*args, **kwargs)

    return _unlock_signal_if_belongs_to_track


class SignalController(Controller):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller)
        self.track = None
        self.base_route = None

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

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    @_signal_belongs_to_track
    def on_unlock(self, track_number):
        self.model.on_unlock()

    def on_save_state(self):
        self.model.on_save_state()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_change_state(self.model.state, self.model.locked)

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_switch_to_green(self, train_route):
        self.model.on_switch_to_green(train_route)

    def on_switch_to_red(self, train_route):
        self.model.on_switch_to_red(train_route)
