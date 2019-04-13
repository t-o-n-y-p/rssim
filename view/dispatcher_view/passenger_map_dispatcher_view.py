from view.dispatcher_view import DispatcherView


class PassengerMapDispatcherView(DispatcherView):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
