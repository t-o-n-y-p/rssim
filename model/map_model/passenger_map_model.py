from random import choice, seed

from model.map_model import MapModel
from controller.train_controller.passenger_train_controller import PassengerTrainController
from model.train_model.passenger_train_model import PassengerTrainModel
from view.train_view.passenger_train_view import PassengerTrainView
from ui.fade_animation.fade_in_animation.train_fade_in_animation import TrainFadeInAnimation
from ui.fade_animation.fade_out_animation.train_fade_out_animation import TrainFadeOutAnimation


class PassengerMapModel(MapModel):
    def __init__(self):
        super().__init__(map_id=0)

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        controller = PassengerTrainController(self.controller, train_id)
        controller.fade_in_animation = TrainFadeInAnimation(controller)
        controller.fade_out_animation = TrainFadeOutAnimation(controller)
        self.controller.fade_in_animation.train_fade_in_animations.append(controller.fade_in_animation)
        self.controller.fade_out_animation.train_fade_out_animations.append(controller.fade_out_animation)
        model = PassengerTrainModel(train_id)
        # car collection is chosen randomly from available options, seed() initializes PRNG
        seed()
        model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                            priority, boarding_time, exp, money, choice(self.unlocked_car_collections))
        view = PassengerTrainView(train_id)
        controller.model = model
        model.controller = controller
        controller.view = view
        view.controller = controller
        model.view = view
        return controller
