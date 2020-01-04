from typing import final

from controller.railroad_switch_controller import RailroadSwitchController
from model.railroad_switch_model.passenger_map_railroad_switch_model import PassengerMapRailroadSwitchModel
from view.railroad_switch_view.passenger_map_railroad_switch_view import PassengerMapRailroadSwitchView
from database import PASSENGER_MAP


@final
class PassengerMapRailroadSwitchController(RailroadSwitchController):
    def __init__(self, map_controller, track_param_1, track_param_2, switch_type):
        super().__init__(*self.create_switch_elements(track_param_1, track_param_2, switch_type),
                         map_id=PASSENGER_MAP, parent_controller=map_controller,
                         track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type)

    def create_switch_elements(self, track_param_1, track_param_2, switch_type):
        view = PassengerMapRailroadSwitchView(controller=self, track_param_1=track_param_1,
                                              track_param_2=track_param_2, switch_type=switch_type)
        model = PassengerMapRailroadSwitchModel(controller=self, view=view, track_param_1=track_param_1,
                                                track_param_2=track_param_2, switch_type=switch_type)
        return model, view
