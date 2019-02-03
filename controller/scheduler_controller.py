from controller import *


class SchedulerController(Controller):
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
        self.parent_controller.on_close_schedule()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_save_state(self):
        self.model.on_save_state()

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    def on_level_up(self, level):
        self.model.on_level_up(level)

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()

    def on_leave_entry(self, entry_id):
        self.model.on_leave_entry(entry_id)