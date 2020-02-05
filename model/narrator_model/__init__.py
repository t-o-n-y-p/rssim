from logging import getLogger

from model import *


class NarratorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.model'))

    def on_save_state(self):
        pass
