from logging import getLogger

from controller import *


class CrossoverController(Controller):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(
            parent_controller=parent_controller,
            logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.controller'
            )
        )
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.crossover_type = crossover_type
        self.map_id = map_id

    @final
    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    @final
    def on_save_state(self):
        self.model.on_save_state()

    @final
    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    @final
    def on_zoom_in(self):
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)

    @final
    def on_zoom_out(self):
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)

    @final
    def on_activate_view(self):
        self.model.on_activate_view()

    @final
    def on_deactivate_view(self):
        self.view.on_deactivate()

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self, positions):
        self.model.on_force_busy_off(positions)

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
    def on_unlock(self):
        self.model.on_unlock()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
