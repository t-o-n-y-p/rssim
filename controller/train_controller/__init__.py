from logging import getLogger

from controller import *
from model.train_model import TrainModel
from view.train_view import TrainView
from ui.fade_animation.fade_in_animation.train_fade_in_animation import TrainFadeInAnimation
from ui.fade_animation.fade_out_animation.train_fade_out_animation import TrainFadeOutAnimation


class TrainController(MapBaseController):
    def __init__(self, model: TrainModel, view: TrainView, map_id, parent_controller, train_id):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.controller'))
        self.train_id = train_id
        self.map_id = map_id
        self.fade_in_animation = TrainFadeInAnimation(self)
        self.fade_out_animation = TrainFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()

    def create_train_elements(self, train_id):
        pass

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
