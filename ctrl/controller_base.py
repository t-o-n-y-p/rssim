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


class Controller:
    def __init__(self, parent_controller=None):
        self.model = None
        self.view = None
        self.is_activated = False
        self.parent_controller = parent_controller
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []

    def on_update_model(self):
        pass

    def on_update_view(self):
        pass

    @_controller_is_not_active
    def on_activate(self):
        pass

    @_controller_is_active
    def on_deactivate(self):
        pass

    def on_append_handlers(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                           on_mouse_release_handlers=None, on_mouse_drag_handlers=None, on_mouse_leave_handlers=None):
        if on_mouse_motion_handlers is not None:
            self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)

        if on_mouse_press_handlers is not None:
            self.on_mouse_press_handlers.extend(on_mouse_press_handlers)

        if on_mouse_release_handlers is not None:
            self.on_mouse_release_handlers.extend(on_mouse_release_handlers)

        if on_mouse_drag_handlers is not None:
            self.on_mouse_drag_handlers.extend(on_mouse_drag_handlers)

        if on_mouse_leave_handlers is not None:
            self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)

        if self.parent_controller is not None:
            self.parent_controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)
