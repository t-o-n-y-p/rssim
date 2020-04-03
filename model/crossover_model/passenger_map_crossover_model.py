from typing import final

from model.crossover_model import CrossoverModel
from database import PASSENGER_MAP


@final
class PassengerMapCrossoverModel(CrossoverModel):
    def __init__(self, controller, view, track_param_1, track_param_2, crossover_type):
        super().__init__(
            controller, view, map_id=PASSENGER_MAP,
            track_param_1=track_param_1, track_param_2=track_param_2, crossover_type=crossover_type
        )
