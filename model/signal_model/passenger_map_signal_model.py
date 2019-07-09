from model.signal_model import SignalModel


class PassengerMapSignalModel(SignalModel):
    def __init__(self, track, base_route):
        super().__init__(map_id=0, track=track, base_route=base_route)
