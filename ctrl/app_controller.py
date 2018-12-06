from sys import exit

from .controller_base import Controller


class AppController(Controller):
    def __init__(self):
        super().__init__()
        self.game = None
        self.settings = None

    def on_update_model(self):
        self.model.on_update()
        self.game.on_update_model()
        self.settings.on_update_model()

    def on_update_view(self):
        self.view.on_update()
        self.game.on_update_view()
        self.settings.on_update_view()

    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.view.on_activate()
        self.game.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.game.on_deactivate()
        self.settings.on_deactivate()

    def on_fullscreen_mode_turned_on(self):
        self.on_change_screen_resolution(self.model.fullscreen_resolution, fullscreen_mode=False)
        self.model.on_fullscreen_mode_turned_on()

    def on_change_screen_resolution(self, screen_resolution, fullscreen_mode):
        self.model.on_change_screen_resolution(screen_resolution, fullscreen_mode)
        self.game.on_change_screen_resolution(screen_resolution)
        self.settings.on_change_screen_resolution(screen_resolution)

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.model.windowed_resolution, fullscreen_mode=False)

    def on_close_game(self):
        self.on_deactivate()
        exit()

    def on_activate_main_menu_view(self):
        pass

    def on_activate_game_view(self):
        self.game.on_activate_view()

    def on_deactivate_current_view(self):
        if self.game.view.is_activated:
            self.game.on_deactivate_view()
            self.settings.navigated_from_game = True

    def on_activate_open_settings_button(self):
        self.view.open_settings_button.on_activate()
