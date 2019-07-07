from view.signal_view import SignalView


class PassengerMapSignalView(SignalView):
    def __init__(self, track, base_route):
        super().__init__(map_id=0, track=track, base_route=base_route)
