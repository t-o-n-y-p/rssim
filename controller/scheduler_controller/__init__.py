from logging import getLogger

from controller import *


class SchedulerController(Controller):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.scheduler.controller'))
        self.map_id = map_id

    @final
    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    @final
    def on_save_state(self):
        self.model.on_save_state()

    @final
    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    @final
    def on_level_up(self, level):
        self.model.on_level_up(level)

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)

    @final
    def on_activate_view(self):
        self.model.on_activate_view()

    @final
    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()

    @final
    def on_leave_entry(self, entry_id):
        self.model.on_leave_entry(entry_id)

    @final
    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    @final
    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    @final
    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)

    @final
    def on_update_clock_state(self, clock_24h_enabled):
        self.view.on_update_clock_state(clock_24h_enabled)
