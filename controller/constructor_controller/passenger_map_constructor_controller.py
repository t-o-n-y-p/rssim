from typing import final

from controller.constructor_controller import ConstructorController
from model.constructor_model.passenger_map_constructor_model import PassengerMapConstructorModel
from view.constructor_view.passenger_map_constructor_view import PassengerMapConstructorView
from database import PASSENGER_MAP


@final
class PassengerMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(map_id=PASSENGER_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = PassengerMapConstructorView(controller=self)
        model = PassengerMapConstructorModel(controller=self, view=view)
        view.construction_state_matrix = model.construction_state_matrix
        return view, model
