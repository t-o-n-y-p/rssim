from controller.railroad_switch_controller import RailroadSwitchController


class PassengerMapRailroadSwitchController(RailroadSwitchController):
    """
    Implements Railroad switch controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller, track_param_1, track_param_2, switch_type):
        super().__init__(map_id=0, parent_controller=map_controller,
                         track_param_1=track_param_1, track_param_2=track_param_2, switch_type=switch_type)
