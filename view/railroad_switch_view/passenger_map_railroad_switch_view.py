from typing import final

from view.railroad_switch_view import RailroadSwitchView
from database import PASSENGER_MAP


@final
class PassengerMapRailroadSwitchView(RailroadSwitchView):
    def __init__(self, controller, track_param_1, track_param_2, switch_type):
        super().__init__(
            controller, map_id=PASSENGER_MAP,
            track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type
        )
