from typing import final

from model.signal_model import SignalModel
from database import PASSENGER_MAP


@final
class PassengerMapSignalModel(SignalModel):
    def __init__(self, controller, view, track, base_route):
        super().__init__(controller, view, map_id=PASSENGER_MAP, track=track, base_route=base_route)
