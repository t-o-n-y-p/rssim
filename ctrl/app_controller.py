from .controller_base import Controller


class AppController(Controller):
    def __init__(self):
        super().__init__()
        self.to_be_activated_during_startup = True

    def on_fullscreen_mode_turned_on(self):
        self.model.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()

    def on_close_game(self):
        self.on_deactivate()
