from .controller_base import Controller


class GameController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app)
        self.map = None

    def on_update_model(self):
        self.model.on_update()
        self.map.on_update_model()

    def on_update_view(self):
        self.view.on_update()
        self.map.on_update_view()

    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.view.on_activate()
        self.map.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.map.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)
        self.map.on_change_screen_resolution(screen_resolution)

    def on_pause_game(self):
        self.model.on_pause_game()
        self.map.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()
        self.map.on_resume_game()

    def on_unlock_track(self, track_number):
        self.map.on_unlock_track(track_number)
