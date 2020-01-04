from typing import final

from model.scheduler_model import SchedulerModel
from database import FREIGHT_MAP


@final
class FreightMapSchedulerModel(SchedulerModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)
