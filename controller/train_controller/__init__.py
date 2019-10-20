from logging import getLogger

from controller import *


class TrainController(AppBaseController, GameBaseController):
    def __init__(self, map_id, parent_controller, train_id):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.controller'))
        self.train_id = train_id
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
    def on_set_train_start_point(self, first_car_start_point):
        self.model.on_set_train_start_point(first_car_start_point)

    @final
    def on_set_train_stop_point(self, first_car_stop_point):
        self.model.on_set_train_stop_point(first_car_stop_point)

    @final
    def on_set_train_destination_point(self, first_car_destination_point):
        self.model.on_set_train_destination_point(first_car_destination_point)

    @final
    def on_set_trail_points(self, trail_points_v2_head_tail, trail_points_v2_mid):
        self.model.on_set_trail_points(trail_points_v2_head_tail, trail_points_v2_mid)

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
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
