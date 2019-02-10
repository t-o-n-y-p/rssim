from logging import getLogger

from controller import *


class TrainController(Controller):
    def __init__(self, map_controller, train_id):
        super().__init__(parent_controller=map_controller,
                         logger=getLogger(f'root.app.game.map.train.{train_id}.controller'))
        self.train_id = train_id

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
