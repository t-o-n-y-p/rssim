from model.railroad_switch_model import RailroadSwitchModel


class PassengerMapRailroadSwitchModel(RailroadSwitchModel):
    def __init__(self, track_param_1, track_param_2, switch_type):
        super().__init__(map_id=0, track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type)
