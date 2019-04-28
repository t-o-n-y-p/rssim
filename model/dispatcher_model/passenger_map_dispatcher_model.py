from model.dispatcher_model import DispatcherModel


class PassengerMapDispatcherModel(DispatcherModel):
    """
    Implements Dispatcher model for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
