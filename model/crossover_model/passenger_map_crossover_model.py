from model.crossover_model import CrossoverModel


class PassengerMapCrossoverModel(CrossoverModel):
    def __init__(self, track_param_1, track_param_2, crossover_type):
        super().__init__(map_id=0, track_param_1=track_param_1, track_param_2=track_param_2,
                         crossover_type=crossover_type)
