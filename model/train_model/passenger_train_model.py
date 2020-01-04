from typing import final

from model.train_model import TrainModel
from model import PASSENGER_CAR_LENGTH, PASSENGER_TRAIN_ACCELERATION_FACTOR
from database import PASSENGER_MAP


@final
class PassengerTrainModel(TrainModel):
    def __init__(self, controller, view, train_id):
        super().__init__(controller, view, map_id=PASSENGER_MAP, train_id=train_id)
        self.train_acceleration_factor = PASSENGER_TRAIN_ACCELERATION_FACTOR
        self.train_maximum_speed = PASSENGER_TRAIN_ACCELERATION_FACTOR[-1] - PASSENGER_TRAIN_ACCELERATION_FACTOR[-2]
        self.speed_factor_position_limit = len(PASSENGER_TRAIN_ACCELERATION_FACTOR) - 1

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(float(first_car_start_point - i * PASSENGER_CAR_LENGTH))
