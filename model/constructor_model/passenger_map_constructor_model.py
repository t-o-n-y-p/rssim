from typing import final

from model.constructor_model import ConstructorModel
from database import PASSENGER_MAP


@final
class PassengerMapConstructorModel(ConstructorModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)
