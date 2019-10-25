from typing import final

from view.map_view import MapView


@final
class PassengerMapView(MapView):
    def __init__(self, controller):
        super().__init__(controller, map_id=0)
