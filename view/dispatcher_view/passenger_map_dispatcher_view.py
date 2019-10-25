from typing import final

from view.dispatcher_view import DispatcherView


@final
class PassengerMapDispatcherView(DispatcherView):
    def __init__(self, controller):
        super().__init__(controller, map_id=0)
