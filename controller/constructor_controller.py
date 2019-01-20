from controller import *


class ConstructorController(Controller):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller)

    def on_update_view(self):
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.parent_controller.on_close_constructor()

    def on_save_state(self):
        self.model.on_save_state()

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.parent_controller.on_close_constructor()

    def on_level_up(self, level):
        self.model.on_level_up(level)

    def on_put_track_under_construction(self, track):
        self.model.on_put_track_under_construction(track)

    def on_add_money(self, money):
        self.model.on_add_money(money)

    def on_pay_money(self, money):
        self.model.on_pay_money(money)
