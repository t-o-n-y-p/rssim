from .controller_base import Controller


def _controller_is_active(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


class FPSController(Controller):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller)

    def on_update_view(self):
        self.view.on_update()

    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.view.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    @_controller_is_active
    def on_update_fps(self, fps):
        self.model.on_update_fps(fps)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
