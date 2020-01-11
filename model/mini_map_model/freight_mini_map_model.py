from typing import final

from model.mini_map_model import MiniMapModel
from database import FREIGHT_MAP


@final
class FreightMiniMapModel(MiniMapModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)
