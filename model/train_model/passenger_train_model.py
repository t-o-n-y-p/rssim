from model.train_model import TrainModel
from model import PASSENGER_CAR_LENGTH, PASSENGER_TRAIN_ACCELERATION_FACTOR


class PassengerTrainModel(TrainModel):
    def __init__(self, controller, view, train_id):
        super().__init__(controller, view, map_id=0, train_id=train_id)
        self.train_acceleration_factor = PASSENGER_TRAIN_ACCELERATION_FACTOR
        self.train_maximum_speed = PASSENGER_TRAIN_ACCELERATION_FACTOR[-1] - PASSENGER_TRAIN_ACCELERATION_FACTOR[-2]
        self.speed_factor_position_limit = len(PASSENGER_TRAIN_ACCELERATION_FACTOR) - 1

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(float(first_car_start_point - i * PASSENGER_CAR_LENGTH))

        self.view.car_position = []
        self.cars_position[0] = round(self.cars_position[0] + self.speed, 1)
        self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[0]))
        for i in range(1, len(self.cars_position) - 1):
            self.cars_position[i] = round(self.cars_position[i] + self.speed, 1)
            self.view.car_position.append(self.trail_points_v2.get_mid_car_position(self.cars_position[i]))

        self.cars_position[-1] = round(self.cars_position[-1] + self.speed, 1)
        self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[-1]))
