from typing import final

from controller.train_route_controller import TrainRouteController
from model.train_route_model.freight_train_route_model import FreightTrainRouteModel
from view.train_route_view.freight_train_route_view import FreightTrainRouteView
from database import FREIGHT_MAP


@final
class FreightTrainRouteController(TrainRouteController):
    def __init__(self, map_controller, track, train_route):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=map_controller, track=track, train_route=train_route)

    def create_view_and_model(self, track, train_route):
        view = FreightTrainRouteView(controller=self, track=track, train_route=train_route)
        model = FreightTrainRouteModel(controller=self, view=view, track=track, train_route=train_route)
        return view, model
