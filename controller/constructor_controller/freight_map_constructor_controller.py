from typing import final

from controller.constructor_controller import ConstructorController
from model.constructor_model.freight_map_constructor_model import FreightMapConstructorModel
from view.constructor_view.freight_map_constructor_view import FreightMapConstructorView
from database import FREIGHT_MAP


@final
class FreightMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = FreightMapConstructorView(controller=self)
        model = FreightMapConstructorModel(controller=self, view=view)
        view.construction_state_matrix = model.construction_state_matrix
        return view, model
