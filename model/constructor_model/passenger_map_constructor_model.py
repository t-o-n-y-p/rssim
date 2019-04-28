from model.constructor_model import ConstructorModel


class PassengerMapConstructorModel(ConstructorModel):
    """
    Implements Constructor model for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
