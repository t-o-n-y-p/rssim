from typing import final

from controller.train_route_controller import TrainRouteController
from model.train_route_model.passenger_train_route_model import PassengerTrainRouteModel
from view.train_route_view.passenger_train_route_view import PassengerTrainRouteView


@final
class PassengerTrainRouteController(TrainRouteController):
    def __init__(self, map_controller, track, train_route):
        super().__init__(*self.create_train_route_elements(track, train_route), map_id=0,
                         parent_controller=map_controller, track=track, train_route=train_route)

    def create_train_route_elements(self, track, train_route):
        view = PassengerTrainRouteView(controller=self, track=track, train_route=train_route)
        model = PassengerTrainRouteModel(controller=self, view=view, track=track, train_route=train_route)
        return model, view
