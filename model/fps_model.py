from model import Model


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


class FPSModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.fps = 0

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.view.on_activate()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_update_fps(self, fps):
        self.fps = fps
        self.view.on_update_fps(fps)
