from typing import final

from controller.railroad_switch_controller import RailroadSwitchController
from model.railroad_switch_model.freight_map_railroad_switch_model import FreightMapRailroadSwitchModel
from view.railroad_switch_view.freight_map_railroad_switch_view import FreightMapRailroadSwitchView
from database import FREIGHT_MAP


@final
class FreightMapRailroadSwitchController(RailroadSwitchController):
    def __init__(self, map_controller, track_param_1, track_param_2, switch_type):
        super().__init__(
            map_id=FREIGHT_MAP, parent_controller=map_controller,
            track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type
        )

    def create_view_and_model(self, track_param_1, track_param_2, switch_type):
        view = FreightMapRailroadSwitchView(
            controller=self, track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type
        )
        model = FreightMapRailroadSwitchModel(
            controller=self, view=view, track_param_1=track_param_1,
            track_param_2=track_param_2, switch_type=switch_type
        )
        return view, model
