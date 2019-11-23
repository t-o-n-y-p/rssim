from logging import getLogger

from model import *
from database import MAP_SWITCHER_STATE_MATRIX


class MapSwitcherModel(GameBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.game.map_switcher.model'))
        self.map_switcher_state_matrix = MAP_SWITCHER_STATE_MATRIX