from typing import final

from model.map_model import MapModel
from controller.train_controller.passenger_train_controller import PassengerTrainController
from database import PASSENGER_MAP


@final
class PassengerMapModel(MapModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)

    def on_create_train(
            self, train_id, cars, track, train_route, state, direction, new_direction,
            current_direction, priority, boarding_time, exp, money, switch_direction_required
    ):
        controller = PassengerTrainController(self.controller, train_id)
        self.controller.fade_in_animation.train_fade_in_animations.append(controller.fade_in_animation)
        self.controller.fade_out_animation.train_fade_out_animations.append(controller.fade_out_animation)
        controller.model.on_train_init(
            cars, track, train_route, state, direction, new_direction, current_direction, priority, boarding_time,
            exp, money, self.unlocked_car_collections[0], switch_direction_required, self.exp_bonus_multiplier,
            self.money_bonus_multiplier, self.game_time, self.game_time_fraction, self.dt_multiplier
        )
        self.unlocked_car_collections.append(self.unlocked_car_collections.pop(0))
        return controller
