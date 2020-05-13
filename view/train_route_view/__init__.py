from abc import ABC
from logging import getLogger

from view import MapBaseView


class TrainRouteView(MapBaseView, ABC):
    def __init__(self, controller, map_id, track, train_route):
        super().__init__(
            controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.view')
        )
        self.track, self.train_route = track, train_route
        self.on_append_window_handlers()
