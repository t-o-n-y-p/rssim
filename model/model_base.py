class Model:
    def __init__(self, game_config):
        self.view = None
        self.is_activated = False
        self.game_config = game_config

    def on_update(self):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_assign_view(self, view):
        pass
