from logging import getLogger

from controller import *


class TrainController(AppBaseController, GameBaseController, MapBaseController):
    def __init__(self, map_id, parent_controller, train_id):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.controller'))
        self.train_id = train_id
        self.map_id = map_id

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
