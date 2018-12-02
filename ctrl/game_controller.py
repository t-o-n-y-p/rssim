from .controller_base import Controller


class GameController(Controller):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller)
        self.to_be_activated_during_startup = True

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)
        for controller in self.child_controllers:
            controller.on_change_screen_resolution(screen_resolution)

    def on_pause_game(self):
        self.model.on_pause_game()
        for controller in self.child_controllers:
            controller.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()
        for controller in self.child_controllers:
            controller.on_resume_game()
