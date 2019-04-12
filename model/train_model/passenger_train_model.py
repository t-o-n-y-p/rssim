from model.train_model import TrainModel
from model import PASSENGER_CAR_LENGTH


class PassengerTrainModel(TrainModel):
    def __init__(self, train_id):
        super().__init__(train_id)

    def on_update_map_id(self):
        self.map_id = 0

    def on_set_train_start_point(self, first_car_start_point):
        """
        Updates train initial position on train route.

        :param first_car_start_point:           data
        """
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(first_car_start_point - i * PASSENGER_CAR_LENGTH)
