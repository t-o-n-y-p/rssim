from typing import final

from model.signal_model import SignalModel
from database import FREIGHT_MAP


@final
class FreightMapSignalModel(SignalModel):
    def __init__(self, controller, view, track, base_route):
        super().__init__(controller, view, map_id=FREIGHT_MAP, track=track, base_route=base_route)
