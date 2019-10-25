from typing import final

from view.signal_view import SignalView


@final
class PassengerMapSignalView(SignalView):
    def __init__(self, controller, track, base_route):
        super().__init__(controller, map_id=0, track=track, base_route=base_route)
