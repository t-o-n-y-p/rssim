from view.dispatcher_view import DispatcherView


class PassengerMapDispatcherView(DispatcherView):
    """
    Implements Dispatcher view for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
