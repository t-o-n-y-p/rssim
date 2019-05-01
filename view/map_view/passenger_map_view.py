from view.map_view import MapView


class PassengerMapView(MapView):
    """
    Implements Map view for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
