from typing import final

from controller.constructor_controller import ConstructorController
from model.constructor_model.freight_map_constructor_model import FreightMapConstructorModel
from view.constructor_view.freight_map_constructor_view import FreightMapConstructorView
from database import FREIGHT_MAP


@final
class FreightMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(*self.create_constructor_elements(), map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_constructor_elements(self):
        view = FreightMapConstructorView(controller=self)
        model = FreightMapConstructorModel(controller=self, view=view)
        return model, view
