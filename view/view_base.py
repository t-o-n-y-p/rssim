class View:
    def __init__(self, game_config, surface, batch, groups):
        self.controller = None
        self.game_config = game_config
        self.surface = surface
        self.batch = batch
        self.groups = groups
        self.is_activated = False
        self.buttons = []

    def on_update(self):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_assign_controller(self, controller):
        self.controller = controller
        self.controller.on_append_handlers_from_buttons()
