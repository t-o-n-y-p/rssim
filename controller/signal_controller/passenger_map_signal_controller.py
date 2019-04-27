from controller.signal_controller import SignalController


class PassengerMapSignalController(SignalController):
    """
    Implements Signal controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller, track, base_route):
        super().__init__(map_id=0, parent_controller=map_controller, track=track, base_route=base_route)
