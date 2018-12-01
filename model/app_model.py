from .model_base import Model


class AppModel(Model):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.screen_resolution = None
        self.is_activated = True

    def on_activate(self):
        self.is_activated = True
        self.screen_resolution = self.game_config.screen_resolution

    def on_assign_view(self, view):
        self.view = view
        self.view.on_change_screen_resolution(self.screen_resolution)
