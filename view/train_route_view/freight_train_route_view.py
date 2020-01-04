from typing import final

from view.train_route_view import TrainRouteView
from database import FREIGHT_MAP


@final
class FreightTrainRouteView(TrainRouteView):
    def __init__(self, controller, track, train_route):
        super().__init__(controller, map_id=FREIGHT_MAP, track=track, train_route=train_route)
