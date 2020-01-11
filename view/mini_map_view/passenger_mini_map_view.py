from typing import final

from view.mini_map_view import MiniMapView
from database import PASSENGER_MAP


@final
class PassengerMiniMapView(MiniMapView):
    def __init__(self, controller):
        super().__init__(controller, map_id=PASSENGER_MAP)
