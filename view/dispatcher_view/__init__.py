from abc import ABC
from logging import getLogger

from view import MapBaseView


class DispatcherView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.view'))
        self.on_append_window_handlers()
