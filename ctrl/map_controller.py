from .controller_base import Controller


class MapController(Controller):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller)

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)
        for controller in self.child_controllers:
            controller.on_change_screen_resolution(screen_resolution)

    def on_move_map(self, dx, dy):
        self.model.on_change_base_offset(dx, dy)
        for controller in self.child_controllers:
            controller.on_change_base_offset(dx, dy)

    def on_pause_game(self):
        for controller in self.child_controllers:
            controller.on_pause_game()

    def on_resume_game(self):
        for controller in self.child_controllers:
            controller.on_resume_game()

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)
        for controller in self.child_controllers:
            controller.on_unlock_track()
