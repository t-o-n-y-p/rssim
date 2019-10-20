from logging import getLogger

from controller import *


class TrainRouteController(AppBaseController, GameBaseController, MapBaseController):
    def __init__(self, map_id, parent_controller, track, train_route):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.controller'))
        self.track = track
        self.train_route = train_route
        self.map_id = map_id

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
