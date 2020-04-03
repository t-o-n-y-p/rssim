from typing import final

from model.railroad_switch_model import RailroadSwitchModel
from database import PASSENGER_MAP


@final
class PassengerMapRailroadSwitchModel(RailroadSwitchModel):
    def __init__(self, controller, view, track_param_1, track_param_2, switch_type):
        super().__init__(
            controller, view, map_id=PASSENGER_MAP,
            track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type
        )
