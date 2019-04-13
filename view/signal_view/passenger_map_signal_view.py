from view.signal_view import SignalView


class PassengerMapSignalView(SignalView):
    def __init__(self, track, base_route):
        super().__init__(track, base_route)

    def on_update_map_id(self):
        self.map_id = 0
