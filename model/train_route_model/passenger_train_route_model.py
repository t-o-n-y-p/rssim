from typing import final

from model.train_route_model import TrainRouteModel
from database import PASSENGER_MAP


@final
class PassengerTrainRouteModel(TrainRouteModel):
    def __init__(self, controller, view, track, train_route):
        super().__init__(controller, view, map_id=PASSENGER_MAP, track=track, train_route=train_route)
