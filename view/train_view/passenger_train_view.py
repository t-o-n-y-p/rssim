from typing import final

from view.train_view import TrainView
from database import PASSENGER_MAP
from ui import PASSENGER_CAR_HEAD_IMAGE, PASSENGER_CAR_MID_IMAGE, PASSENGER_CAR_TAIL_IMAGE, \
    PASSENGER_BOARDING_LIGHT_IMAGE


@final
class PassengerTrainView(TrainView):
    def __init__(self, controller, train_id):
        super().__init__(controller, map_id=PASSENGER_MAP, train_id=train_id)
        self.car_head_image = PASSENGER_CAR_HEAD_IMAGE
        self.car_mid_image = PASSENGER_CAR_MID_IMAGE
        self.car_tail_image = PASSENGER_CAR_TAIL_IMAGE
        self.boarding_light_image = PASSENGER_BOARDING_LIGHT_IMAGE
