from model.dispatcher_model import DispatcherModel


class PassengerMapDispatcherModel(DispatcherModel):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
