from model.train_route_model import TrainRouteModel


class PassengerTrainRouteModel(TrainRouteModel):
    """
    Implements Train route model for passenger map (map_id = 0).
    """
    def __init__(self, track, train_route):
        super().__init__(map_id=0, track=track, train_route=train_route)
