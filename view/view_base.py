class View:
    def __init__(self, surface, batch, groups):
        self.controller = None
        self.surface = surface
        self.batch = batch
        self.groups = groups
        self.is_activated = False
        self.buttons = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []

    def on_update(self):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_assign_controller(self, controller):
        self.controller = controller
        on_mouse_motion_handlers = []
        on_mouse_press_handlers = []
        on_mouse_release_handlers = []
        on_mouse_leave_handlers = []
        for b in self.buttons:
            on_mouse_motion_handlers.append(b.handle_mouse_motion)
            on_mouse_press_handlers.append(b.handle_mouse_press)
            on_mouse_release_handlers.append(b.handle_mouse_release)
            on_mouse_leave_handlers.append(b.handle_mouse_leave)

        self.controller.on_append_handlers(on_mouse_motion_handlers=self.on_mouse_motion_handlers,
                                           on_mouse_press_handlers=self.on_mouse_press_handlers,
                                           on_mouse_release_handlers=self.on_mouse_release_handlers,
                                           on_mouse_drag_handlers=self.on_mouse_drag_handlers,
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers)
        self.controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                           on_mouse_press_handlers=on_mouse_press_handlers,
                                           on_mouse_release_handlers=on_mouse_release_handlers,
                                           on_mouse_leave_handlers=on_mouse_leave_handlers)
