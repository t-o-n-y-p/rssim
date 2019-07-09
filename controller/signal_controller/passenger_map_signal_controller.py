from controller.signal_controller import SignalController


class PassengerMapSignalController(SignalController):
    def __init__(self, map_controller, track, base_route):
        super().__init__(map_id=0, parent_controller=map_controller, track=track, base_route=base_route)
