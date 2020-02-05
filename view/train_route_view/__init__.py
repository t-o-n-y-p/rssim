from logging import getLogger

from view import *


class TrainRouteView(MapBaseView, ABC):
    def __init__(self, controller, map_id, track, train_route):
        super().__init__(controller, map_id,
                         logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.view'))
        self.track, self.train_route = track, train_route

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
