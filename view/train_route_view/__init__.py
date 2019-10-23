from logging import getLogger

from view import *


class TrainRouteView(MapBaseView):
    def __init__(self, map_id, track, train_route):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.view'))
        self.map_id = map_id

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
