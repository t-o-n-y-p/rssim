from view.crossover_view import CrossoverView


class PassengerMapCrossoverView(CrossoverView):
    def __init__(self, track_param_1, track_param_2, crossover_type):
        super().__init__(track_param_1, track_param_2, crossover_type)

    def on_update_map_id(self):
        self.map_id = 0
