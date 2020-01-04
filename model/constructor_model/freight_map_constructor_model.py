from typing import final

from model.constructor_model import ConstructorModel
from database import FREIGHT_MAP


@final
class FreightMapConstructorModel(ConstructorModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)
