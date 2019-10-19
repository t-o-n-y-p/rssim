from typing import final

from view.dispatcher_view import DispatcherView


@final
class PassengerMapDispatcherView(DispatcherView):
    def __init__(self):
        super().__init__(map_id=0)
