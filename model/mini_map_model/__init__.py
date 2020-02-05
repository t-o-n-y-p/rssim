from logging import getLogger

from model import *


class MiniMapModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.mini_map.model'))

    def on_save_state(self):
        pass
