from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.train_fade_in_animation import TrainFadeInAnimation
from ui.fade_animation.fade_out_animation.train_fade_out_animation import TrainFadeOutAnimation


class TrainController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, train_id):
        super().__init__(
            map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.controller')
        )
        self.view, self.model = self.create_view_and_model(train_id)
        self.train_id = train_id
        self.fade_in_animation = TrainFadeInAnimation(self.view)
        self.fade_out_animation = TrainFadeOutAnimation(self.view)

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
    def on_set_trail_points(self, trail_points_v2):
        self.model.on_set_trail_points(trail_points_v2)

    @final
    def on_train_setup(self):
        self.model.on_train_setup()
