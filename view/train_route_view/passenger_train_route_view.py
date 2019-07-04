from view.train_route_view import TrainRouteView


class PassengerTrainRouteView(TrainRouteView):
    def __init__(self, track, train_route):
        super().__init__(map_id=0, track=track, train_route=train_route)
