from typing import final

from database import FREIGHT_MAP
from model.narrator_model import NarratorModel


@final
class FreightMapNarratorModel(NarratorModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)
