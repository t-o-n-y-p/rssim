from random import choice, seed
from typing import final

from model.map_model import MapModel
from controller.train_controller.passenger_train_controller import PassengerTrainController
from database import PASSENGER_MAP


@final
class PassengerMapModel(MapModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money, switch_direction_required):
        controller = PassengerTrainController(self.controller, train_id)
        self.controller.fade_in_animation.train_fade_in_animations.append(controller.fade_in_animation)
        self.controller.fade_out_animation.train_fade_out_animations.append(controller.fade_out_animation)
        seed()
        controller.model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                                       priority, boarding_time, exp, money, choice(self.unlocked_car_collections),
                                       switch_direction_required, self.exp_bonus_multiplier,
                                       self.money_bonus_multiplier)
        return controller
