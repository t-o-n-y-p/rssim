from view.crossover_view import CrossoverView


class PassengerMapCrossoverView(CrossoverView):
    """
    Implements Crossover view for passenger map (map_id = 0).
    """
    def __init__(self, track_param_1, track_param_2, crossover_type):
        super().__init__(map_id=0, track_param_1=track_param_1, track_param_2=track_param_2,
                         crossover_type=crossover_type)
