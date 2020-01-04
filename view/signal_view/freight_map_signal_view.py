from typing import final

from view.signal_view import SignalView
from database import FREIGHT_MAP


@final
class FreightMapSignalView(SignalView):
    def __init__(self, controller, track, base_route):
        super().__init__(controller, map_id=FREIGHT_MAP, track=track, base_route=base_route)
