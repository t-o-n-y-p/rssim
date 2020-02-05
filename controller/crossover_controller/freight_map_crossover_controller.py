from typing import final

from controller.crossover_controller import CrossoverController
from model.crossover_model.freight_map_crossover_model import FreightMapCrossoverModel
from view.crossover_view.freight_map_crossover_view import FreightMapCrossoverView
from database import FREIGHT_MAP


@final
class FreightMapCrossoverController(CrossoverController):
    def __init__(self, map_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=map_controller,
                         track_param_1=track_param_1, track_param_2=track_param_2, crossover_type=crossover_type)

    def create_view_and_model(self, track_param_1, track_param_2, crossover_type):
        view = FreightMapCrossoverView(controller=self, track_param_1=track_param_1,
                                       track_param_2=track_param_2, crossover_type=crossover_type)
        model = FreightMapCrossoverModel(controller=self, view=view, track_param_1=track_param_1,
                                         track_param_2=track_param_2, crossover_type=crossover_type)
        return view, model
