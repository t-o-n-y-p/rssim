from logging import getLogger

from controller.signal_controller import SignalController


class PassengerMapSignalController(SignalController):
    def __init__(self, map_controller, track, base_route):
        super().__init__(parent_controller=map_controller, track=track, base_route=base_route,
                         logger=getLogger(f'root.app.game.map.0.signal.{track}.{base_route}.controller'))
