def _model_is_activated(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_activated(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class Model:
    def __init__(self, game_config):
        self.view = None
        self.is_activated = False
        self.game_config = game_config

    def on_update(self):
        pass

    @_model_is_not_activated
    def on_activate(self):
        pass

    @_model_is_activated
    def on_deactivate(self):
        pass

    def on_assign_view(self, view):
        pass
