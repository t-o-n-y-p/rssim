from typing import final

from model.train_model import TrainModel
from model import PASSENGER_CAR_LENGTH
from database import PASSENGER_MAP


@final
class PassengerTrainModel(TrainModel):
    def __init__(self, controller, view, train_id):
        super().__init__(controller, view, map_id=PASSENGER_MAP, train_id=train_id)

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(float(first_car_start_point - i * PASSENGER_CAR_LENGTH))
