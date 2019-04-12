from random import choice, seed

from textures import CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE
from model.map_model import MapModel
from controller.train_controller.passenger_train_controller import PassengerTrainController
from model.train_model.passenger_train_model import PassengerTrainModel
from view.train_view import TrainView


class PassengerMapModel(MapModel):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        """
        Creates new train similar to _create_train function.

        :param train_id:                        train identification number
        :param cars:                            number of cars in the train
        :param track:                           track number (0 for regular entry and 100 for side entry)
        :param train_route:                     train route type (left/right approaching or side_approaching)
        :param state:                           train state: approaching or approaching_pass_through
        :param direction:                       train arrival direction
        :param new_direction:                   train departure direction
        :param current_direction:               train current direction
        :param priority:                        train priority in the queue
        :param boarding_time:                   amount of boarding time left for this train
        :param exp:                             exp gained when boarding finishes
        :param money:                           money gained when boarding finishes
        :return:                                Train object controller
        """
        controller = PassengerTrainController(self.controller, train_id)
        model = PassengerTrainModel(train_id)
        # car collection is chosen randomly from available options, seed() initializes PRNG
        seed()
        model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                            priority, boarding_time, exp, money, choice(self.unlocked_car_collections))
        view = TrainView(train_id, CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE)
        controller.model = model
        model.controller = controller
        controller.view = view
        view.on_assign_controller(controller)
        model.view = view
        return controller
