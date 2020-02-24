from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.train_route_fade_in_animation import TrainRouteFadeInAnimation
from ui.fade_animation.fade_out_animation.train_route_fade_out_animation import TrainRouteFadeOutAnimation


class TrainRouteController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, track, train_route):
        super().__init__(map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.controller'))
        self.view, self.model = self.create_view_and_model(track, train_route)
        self.track, self.train_route = track, train_route
        self.fade_in_animation = TrainRouteFadeInAnimation(self.view)
        self.fade_out_animation = TrainRouteFadeOutAnimation(self.view)

    @final
    def on_open_train_route(self, train_id, cars):
        self.model.on_open_train_route(train_id, cars)

    @final
    def on_close_train_route(self):
        self.model.on_close_train_route()

    @final
    def on_update_train_route_sections(self, last_car_position):
        self.model.on_update_train_route_sections(last_car_position)

    @final
    def on_update_priority(self, priority):
        self.model.on_update_priority(priority)

    @final
    def on_update_section_status(self, section, status):
        self.model.on_update_section_status(section, status)
