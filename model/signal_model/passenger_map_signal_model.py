from model.signal_model import SignalModel


class PassengerMapSignalModel(SignalModel):
    def __init__(self, track, base_route):
        super().__init__(track, base_route)

    def on_update_map_id(self):
        self.map_id = 0
