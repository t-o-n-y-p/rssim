from typing import final

from controller.crossover_controller import CrossoverController
from model.crossover_model.passenger_map_crossover_model import PassengerMapCrossoverModel
from view.crossover_view.passenger_map_crossover_view import PassengerMapCrossoverView
from database import PASSENGER_MAP


@final
class PassengerMapCrossoverController(CrossoverController):
    def __init__(self, map_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(*self.create_crossover_elements(track_param_1, track_param_2, crossover_type),
                         map_id=PASSENGER_MAP, parent_controller=map_controller,
                         track_param_1=track_param_1, track_param_2=track_param_2, crossover_type=crossover_type)

    def create_crossover_elements(self, track_param_1, track_param_2, crossover_type):
        view = PassengerMapCrossoverView(controller=self, track_param_1=track_param_1,
                                         track_param_2=track_param_2, crossover_type=crossover_type)
        model = PassengerMapCrossoverModel(controller=self, view=view, track_param_1=track_param_1,
                                           track_param_2=track_param_2, crossover_type=crossover_type)
        return model, view
