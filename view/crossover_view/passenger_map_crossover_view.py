from typing import final

from view.crossover_view import CrossoverView


@final
class PassengerMapCrossoverView(CrossoverView):
    def __init__(self, controller, track_param_1, track_param_2, crossover_type):
        super().__init__(controller, map_id=0, track_param_1=track_param_1, track_param_2=track_param_2,
                         crossover_type=crossover_type)
