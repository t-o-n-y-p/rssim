from view.railroad_switch_view import RailroadSwitchView


class PassengerMapRailroadSwitchView(RailroadSwitchView):
    def __init__(self, track_param_1, track_param_2, switch_type):
        super().__init__(track_param_1, track_param_2, switch_type)

    def on_update_map_id(self):
        self.map_id = 0
