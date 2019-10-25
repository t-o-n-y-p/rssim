from model.constructor_model import ConstructorModel


class PassengerMapConstructorModel(ConstructorModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=0)
