from typing import final

from controller.constructor_controller import ConstructorController


@final
class PassengerMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(map_id=0, parent_controller=map_controller)
