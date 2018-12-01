from sys import exit


def _controller_is_activated(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def _controller_is_not_activated(fn):
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


class Controller:
    def __init__(self, parent_controller=None):
        self.model = None
        self.view = None
        self.to_be_activated_during_startup = None
        self.is_activated = False
        self.parent_controller = parent_controller
        self.child_controllers = []
        self.exclusive_child_controllers = []
        self.init_controllers = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []

    def on_update_model(self):
        self.model.on_update()
        for controller in self.child_controllers:
            controller.on_update_model()

    def on_update_view(self):
        self.view.on_update()
        for controller in self.child_controllers:
            controller.on_update_view()

    @_controller_is_not_activated
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.view.on_activate()
        for controller in self.init_controllers:
            controller.on_activate()

    @_controller_is_activated
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        for controller in self.child_controllers:
            controller.on_deactivate()

        if self.parent_controller is None:
            exit()

    def on_activate_child_controller(self, controller):
        if controller in self.exclusive_child_controllers:
            for c in self.exclusive_child_controllers:
                c.on_deactivate()

        controller.on_activate()

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
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)
