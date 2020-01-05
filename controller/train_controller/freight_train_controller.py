from typing import final

from controller.train_controller import TrainController
from model.train_model.freight_train_model import FreightTrainModel
from view.train_view.freight_train_view import FreightTrainView
from database import FREIGHT_MAP


@final
class FreightTrainController(TrainController):
    def __init__(self, map_controller, train_id):
        super().__init__(*self.create_train_elements(train_id),
                         map_id=FREIGHT_MAP, parent_controller=map_controller, train_id=train_id)

    def create_train_elements(self, train_id):
        view = FreightTrainView(controller=self, train_id=train_id)
        model = FreightTrainModel(controller=self, view=view, train_id=train_id)
        return model, view
