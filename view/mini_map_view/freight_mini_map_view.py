from typing import final

from view.mini_map_view import MiniMapView
from database import FREIGHT_MAP


@final
class FreightMiniMapView(MiniMapView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
