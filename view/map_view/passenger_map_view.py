from view.map_view import MapView


class PassengerMapView(MapView):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
