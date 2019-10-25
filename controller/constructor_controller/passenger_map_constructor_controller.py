from typing import final

from controller.constructor_controller import ConstructorController
from model.constructor_model.passenger_map_constructor_model import PassengerMapConstructorModel
from view.constructor_view.passenger_map_constructor_view import PassengerMapConstructorView


@final
class PassengerMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(*self.create_constructor_elements(), map_id=0, parent_controller=map_controller)

    def create_constructor_elements(self):
        view = PassengerMapConstructorView(controller=self)
        model = PassengerMapConstructorModel(controller=self, view=view)
        return model, view
