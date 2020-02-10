from logging import getLogger

from view import *


class NarratorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
        self.on_append_window_handlers()
