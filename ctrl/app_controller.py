from .controller_base import Controller


class AppController(Controller):
    def __init__(self):
        super().__init__()
        self.to_be_activated_during_startup = True

    def on_fullscreen_mode_turned_on(self):
        self.on_change_screen_resolution(self.model.fullscreen_resolution, fullscreen_mode=False)
        self.model.on_fullscreen_mode_turned_on()

    def on_change_screen_resolution(self, screen_resolution, fullscreen_mode):
        self.model.on_change_screen_resolution(screen_resolution, fullscreen_mode)
        for controller in self.child_controllers:
            controller.on_change_screen_resolution(screen_resolution)

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.model.windowed_resolution, fullscreen_mode=False)

    def on_close_game(self):
        for controller in self.child_controllers:
            controller.on_deactivate()

        self.on_deactivate()
