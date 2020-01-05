from typing import final

from controller.train_controller import TrainController
from model.train_model.passenger_train_model import PassengerTrainModel
from view.train_view.passenger_train_view import PassengerTrainView
from database import PASSENGER_MAP


@final
class PassengerTrainController(TrainController):
    def __init__(self, map_controller, train_id):
        super().__init__(*self.create_train_elements(train_id),
                         map_id=PASSENGER_MAP, parent_controller=map_controller, train_id=train_id)

    def create_train_elements(self, train_id):
        view = PassengerTrainView(controller=self, train_id=train_id)
        model = PassengerTrainModel(controller=self, view=view, train_id=train_id)
        return model, view
