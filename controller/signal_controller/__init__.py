from logging import getLogger

from controller import *


class SignalController(MapBaseController):
    def __init__(self, map_id, parent_controller, track, base_route):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.controller'))
        self.track = track
        self.base_route = base_route
        self.map_id = map_id

    @final
    def on_switch_to_green(self):
        self.model.on_switch_to_green()

    @final
    def on_switch_to_red(self):
        self.model.on_switch_to_red()
