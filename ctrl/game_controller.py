from .controller_base import Controller


def _game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[0].model.game_paused:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


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


class GameController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app)
        self.map = None

    def on_update_view(self):
        self.view.on_update()
        self.map.on_update_view()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.map.on_activate()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.map.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.map.on_change_screen_resolution(screen_resolution)

    def on_pause_game(self):
        self.model.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()

    def on_unlock_track(self, track_number):
        self.map.on_unlock_track(track_number)

    def on_activate_view(self):
        self.model.on_activate_view()
        self.map.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.map.on_deactivate_view()

    @_controller_is_active
    @_game_is_not_paused
    def on_update_time(self):
        self.map.on_update_time(self.model.game_time)
        self.model.on_update_time()
        if self.model.game_time % 28800 == 0:
            self.on_save_and_commit_state()

    def on_save_and_commit_state(self):
        self.model.on_save_state()
        self.map.on_save_state()

        self.model.user_db_connection.commit()

    def on_level_up(self):
        self.model.on_level_up()
        self.map.on_level_up()

    def on_update_money_target(self, money_target):
        self.model.on_update_money_target(money_target)

    def on_add_exp(self, exp):
        self.model.on_add_exp(exp)

    def on_add_money(self, money):
        self.model.on_add_money(money)
