from logging import getLogger

from controller.train_route_controller import TrainRouteController


class PassengerTrainRouteController(TrainRouteController):
    def __init__(self, map_controller, track, train_route):
        super().__init__(parent_controller=map_controller, track=track, train_route=train_route,
                         logger=getLogger(f'root.app.game.map.0.train_route.{track}.{train_route}.controller'))
