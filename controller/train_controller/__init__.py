from logging import getLogger

from controller import *


class TrainController(Controller):
    def __init__(self, map_id, parent_controller, train_id):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.controller'))
        self.train_id = train_id
        self.map_id = map_id

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_save_state(self):
        self.model.on_save_state()

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

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

    def on_set_train_start_point(self, first_car_start_point):
        self.model.on_set_train_start_point(first_car_start_point)

    def on_set_train_stop_point(self, first_car_stop_point):
        self.model.on_set_train_stop_point(first_car_stop_point)

    def on_set_train_destination_point(self, first_car_destination_point):
        self.model.on_set_train_destination_point(first_car_destination_point)

    def on_set_trail_points(self, trail_points_v2):
        self.model.on_set_trail_points(trail_points_v2)

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
