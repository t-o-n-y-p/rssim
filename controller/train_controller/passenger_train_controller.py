from typing import final

from controller.train_controller import TrainController
from model.train_model.passenger_train_model import PassengerTrainModel
from view.train_view.passenger_train_view import PassengerTrainView


@final
class PassengerTrainController(TrainController):
    def __init__(self, map_controller, train_id, database_mode=True):
        super().__init__(*self.create_train_elements(train_id, database_mode),
                         map_id=0, parent_controller=map_controller, train_id=train_id)

    def create_train_elements(self, train_id, database_mode):
        view = PassengerTrainView(controller=self, train_id=train_id)
        model = PassengerTrainModel(controller=self, view=view, train_id=train_id)
        if database_mode:
            model.on_train_setup()

        return model, view
