from controller.crossover_controller import CrossoverController


class PassengerMapCrossoverController(CrossoverController):
    """
    Implements Crossover controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(map_id=0, parent_controller=map_controller,
                         track_param_1=track_param_1, track_param_2=track_param_2, crossover_type=crossover_type)
