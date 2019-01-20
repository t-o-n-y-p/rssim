from controller import Controller


def _controller_is_active(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def _controller_is_not_active(fn):
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


class SettingsController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app)
        self.navigated_from_main_menu = False
        self.navigated_from_game = False

    def on_update_view(self):
        self.view.on_update()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.parent_controller.on_deactivate_current_view()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        if self.navigated_from_main_menu:
            self.navigated_from_main_menu = False
            self.parent_controller.on_activate_main_menu_view()

        if self.navigated_from_game:
            self.navigated_from_game = False
            self.parent_controller.on_activate_game_view()

        self.parent_controller.on_activate_open_settings_button()

    def on_change_screen_resolution(self, screen_resolution):
        self.model.on_change_screen_resolution(screen_resolution)

    def on_save_and_commit_state(self):
        self.model.on_save_and_commit_state()
