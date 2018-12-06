def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class Model:
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        self.view = None
        self.is_activated = False
        self.user_db_connection = user_db_connection
        self.user_db_cursor = user_db_cursor
        self.config_db_cursor = config_db_cursor

    @_model_is_not_active
    def on_activate(self):
        pass

    @_model_is_active
    def on_deactivate(self):
        pass

    def on_assign_view(self, view):
        pass

    def save_state(self):
        pass
