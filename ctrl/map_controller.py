from .controller_base import Controller


class MapController(Controller):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller)

    def on_update_model(self):
        self.model.on_update()

    def on_update_view(self):
        self.view.on_update()

    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.view.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)

    def on_move_map(self, dx, dy):
        self.model.on_change_base_offset(dx, dy)

    def on_pause_game(self):
        pass

    def on_resume_game(self):
        pass

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)

    def on_activate_view(self):
        self.view.on_activate()

    def on_deactivate_view(self):
        self.view.on_deactivate()
