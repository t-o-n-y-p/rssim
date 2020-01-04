from typing import final

from view.signal_view import SignalView
from database import PASSENGER_MAP


@final
class PassengerMapSignalView(SignalView):
    def __init__(self, controller, track, base_route):
        super().__init__(controller, map_id=PASSENGER_MAP, track=track, base_route=base_route)
