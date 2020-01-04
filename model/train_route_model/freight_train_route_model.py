from typing import final

from model.train_route_model import TrainRouteModel
from database import FREIGHT_MAP


@final
class FreightTrainRouteModel(TrainRouteModel):
    def __init__(self, controller, view, track, train_route):
        super().__init__(controller, view, map_id=FREIGHT_MAP, track=track, train_route=train_route)
