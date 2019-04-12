from model.train_route_model import TrainRouteModel


class PassengerTrainRouteModel(TrainRouteModel):
    def __init__(self, track, train_route):
        super().__init__(track, train_route)

    def on_update_map_id(self):
        self.map_id = 0
