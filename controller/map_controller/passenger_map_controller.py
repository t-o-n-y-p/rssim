from controller.map_controller import MapController


class PassengerMapController(MapController):
    """
    Implements Map controller for passenger map (map_id = 0).
    """
    def __init__(self, game_controller):
        super().__init__(map_id=0, parent_controller=game_controller)
