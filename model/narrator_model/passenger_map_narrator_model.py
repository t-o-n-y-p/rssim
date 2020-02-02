from typing import final

from database import PASSENGER_MAP
from model.narrator_model import NarratorModel


@final
class PassengerMapNarratorModel(NarratorModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)
