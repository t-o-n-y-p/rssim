class Controller:
    def __init__(self, parent_controller=None):
        self.model = None
        self.view = None
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

    def on_activate(self):
        self.model.on_activate()
        self.view.on_activate()
        for controller in self.init_controllers:
            controller.on_activate()

    def on_deactivate(self):
        self.model.on_deactivate()
        self.view.on_deactivate()
        for controller in self.child_controllers:
            controller.on_deactivate()

    def on_activate_child_controller(self, controller):
        if controller in self.exclusive_child_controllers:
            for c in self.exclusive_child_controllers:
                c.on_deactivate()

        controller.on_activate()

    def on_append_handlers_from_buttons(self):
        on_mouse_motion_handlers = []
        on_mouse_press_handlers = []
        on_mouse_release_handlers = []
        on_mouse_leave_handlers = []
        for b in self.view.buttons:
            on_mouse_motion_handlers.append(b.handle_mouse_motion)
            on_mouse_press_handlers.append(b.handle_mouse_press)
            on_mouse_release_handlers.append(b.handle_mouse_release)
            on_mouse_leave_handlers.append(b.handle_mouse_leave)

        self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)
        self.on_mouse_press_handlers.extend(on_mouse_press_handlers)
        self.on_mouse_release_handlers.extend(on_mouse_release_handlers)
        self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)
        if self.parent_controller is not None:
            self.parent_controller\
                .on_append_handlers_from_child_controller(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                          on_mouse_press_handlers=on_mouse_press_handlers,
                                                          on_mouse_release_handlers=on_mouse_release_handlers,
                                                          on_mouse_leave_handlers=on_mouse_leave_handlers)

    def on_append_handlers_from_child_controller(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                                                 on_mouse_release_handlers=None, on_mouse_drag_handlers=None,
                                                 on_mouse_leave_handlers=None):
        self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)
        self.on_mouse_press_handlers.extend(on_mouse_press_handlers)
        self.on_mouse_release_handlers.extend(on_mouse_release_handlers)
        self.on_mouse_drag_handlers.extend(on_mouse_drag_handlers)
        self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)
        if self.parent_controller is not None:
            self.parent_controller\
                .on_append_handlers_from_child_controller(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                          on_mouse_press_handlers=on_mouse_press_handlers,
                                                          on_mouse_release_handlers=on_mouse_release_handlers,
                                                          on_mouse_leave_handlers=on_mouse_leave_handlers)
