from typing import final

from model.scheduler_model import SchedulerModel
from database import PASSENGER_MAP


@final
class PassengerMapSchedulerModel(SchedulerModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=PASSENGER_MAP)
