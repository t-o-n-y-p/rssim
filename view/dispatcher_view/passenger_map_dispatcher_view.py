from view.dispatcher_view import DispatcherView


class PassengerMapDispatcherView(DispatcherView):
    def __init__(self):
        super().__init__(map_id=0)
