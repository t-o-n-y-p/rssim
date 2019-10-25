from typing import final

from view.train_route_view import TrainRouteView


@final
class PassengerTrainRouteView(TrainRouteView):
    def __init__(self, controller, track, train_route):
        super().__init__(controller, map_id=0, track=track, train_route=train_route)
