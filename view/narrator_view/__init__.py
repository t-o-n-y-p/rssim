from logging import getLogger

from view import *


class NarratorView(MapBaseView):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
