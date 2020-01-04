from typing import final

from view.dispatcher_view import DispatcherView
from database import PASSENGER_MAP


@final
class PassengerMapDispatcherView(DispatcherView):
    def __init__(self, controller):
        super().__init__(controller, map_id=PASSENGER_MAP)
