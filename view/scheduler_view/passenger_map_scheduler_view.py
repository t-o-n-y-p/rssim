from typing import final

from view.scheduler_view import SchedulerView
from database import PASSENGER_MAP


@final
class PassengerMapSchedulerView(SchedulerView):
    def __init__(self, controller):
        super().__init__(controller, map_id=PASSENGER_MAP)
