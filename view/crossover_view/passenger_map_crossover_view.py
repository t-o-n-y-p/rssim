from typing import final

from view.crossover_view import CrossoverView
from database import PASSENGER_MAP


@final
class PassengerMapCrossoverView(CrossoverView):
    def __init__(self, controller, track_param_1, track_param_2, crossover_type):
        super().__init__(
            controller, map_id=PASSENGER_MAP, track_param_1=track_param_1, track_param_2=track_param_2,
            crossover_type=crossover_type
        )
