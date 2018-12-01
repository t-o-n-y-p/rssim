def _view_is_activated(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_activated(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


class View:
    def __init__(self, user_db_connection, surface, batch, groups):
        self.controller = None
        self.user_db_connection = user_db_connection
        self.surface = surface
        self.batch = batch
        self.groups = groups
        self.is_activated = False
        self.buttons = []

    def on_update(self):
        pass

    @_view_is_not_activated
    def on_activate(self):
        pass

    @_view_is_activated
    def on_deactivate(self):
        pass

    def on_assign_controller(self, controller):
        self.controller = controller
        self.controller.on_append_handlers_from_buttons()
