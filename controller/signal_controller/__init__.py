from logging import getLogger

from controller import *


class SignalController(Controller):
    def __init__(self, map_id, parent_controller, track, base_route):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.controller'))
        self.track = track
        self.base_route = base_route
        self.map_id = map_id

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_unlock(self):
        self.model.on_unlock()

    def on_save_state(self):
        self.model.on_save_state()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_switch_to_green(self):
        self.model.on_switch_to_green()

    def on_switch_to_red(self):
        self.model.on_switch_to_red()

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
