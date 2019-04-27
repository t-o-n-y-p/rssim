from controller.train_route_controller import TrainRouteController


class PassengerTrainRouteController(TrainRouteController):
    """
    Implements Train route controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller, track, train_route):
        super().__init__(map_id=0, parent_controller=map_controller, track=track, train_route=train_route)
