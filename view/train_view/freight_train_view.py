from typing import final

from view.train_view import TrainView
from database import FREIGHT_MAP
from textures import FREIGHT_CAR_HEAD_IMAGE, FREIGHT_CAR_MID_IMAGE, FREIGHT_CAR_TAIL_IMAGE, \
    FREIGHT_BOARDING_LIGHT_IMAGE


@final
class FreightTrainView(TrainView):
    def __init__(self, controller, train_id):
        super().__init__(controller, map_id=FREIGHT_MAP, train_id=train_id)
        self.car_head_image = FREIGHT_CAR_HEAD_IMAGE
        self.car_mid_image = FREIGHT_CAR_MID_IMAGE
        self.car_tail_image = FREIGHT_CAR_TAIL_IMAGE
        self.boarding_light_image = FREIGHT_BOARDING_LIGHT_IMAGE
