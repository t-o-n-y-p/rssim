from logging import getLogger

from controller import *


class RailroadSwitchController(Controller):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, switch_type):
        logger_name \
            = f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.controller'
        super().__init__(parent_controller=parent_controller, logger=getLogger(logger_name))
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.switch_type = switch_type
        self.map_id = map_id

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_save_state(self):
        self.model.on_save_state()

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    def on_force_busy_off(self):
        self.model.on_force_busy_off()

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_unlock(self):
        self.model.on_unlock()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
