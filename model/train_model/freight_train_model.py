from typing import final

from model.train_model import TrainModel
from model import FREIGHT_HEAD_TAIL_CAR_LENGTH, FREIGHT_MID_CAR_LENGTH
from database import FREIGHT_MAP


@final
class FreightTrainModel(TrainModel):
    def __init__(self, controller, view, train_id):
        super().__init__(controller, view, map_id=FREIGHT_MAP, train_id=train_id)

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = []
        self.cars_position.append(float(first_car_start_point))
        for i in range(self.cars - 2):
            self.cars_position.append(
                float(first_car_start_point) - (FREIGHT_HEAD_TAIL_CAR_LENGTH // 2 + FREIGHT_MID_CAR_LENGTH // 2 + 1)
                - i * FREIGHT_MID_CAR_LENGTH
            )

        self.cars_position.append(
            float(first_car_start_point) - 2 * (FREIGHT_HEAD_TAIL_CAR_LENGTH // 2 + FREIGHT_MID_CAR_LENGTH // 2 + 1)
            - (self.cars - 3) * FREIGHT_MID_CAR_LENGTH
        )
