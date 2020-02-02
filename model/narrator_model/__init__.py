from logging import getLogger

from model import *


class NarratorModel(MapBaseModel):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.model'))
