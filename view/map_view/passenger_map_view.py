from typing import final

from view.map_view import MapView


@final
class PassengerMapView(MapView):
    def __init__(self):
        super().__init__(map_id=0)
