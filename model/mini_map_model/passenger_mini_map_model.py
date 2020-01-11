from typing import final

from model.mini_map_model import MiniMapModel
from database import PASSENGER_MAP


@final
class PassengerMiniMapModel(MiniMapModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)
