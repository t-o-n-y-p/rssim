from model.constructor_model import ConstructorModel


class PassengerMapConstructorModel(ConstructorModel):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
