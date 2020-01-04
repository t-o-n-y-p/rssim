from typing import final

from view.map_view import MapView
from database import FREIGHT_MAP


@final
class FreightMapView(MapView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
