from logging import getLogger

from controller.map_controller import MapController


class PassengerMapController(MapController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller, logger=getLogger('root.app.game.map.0.controller'))
