from typing import final

from controller.map_controller import MapController


@final
class PassengerMapController(MapController):
    def __init__(self, game_controller):
        super().__init__(map_id=0, parent_controller=game_controller)
