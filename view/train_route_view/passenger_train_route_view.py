from view.train_route_view import TrainRouteView


class PassengerTrainRouteView(TrainRouteView):
    def __init__(self, track, train_route):
        super().__init__(track, train_route)

    def on_update_map_id(self):
        self.map_id = 0
