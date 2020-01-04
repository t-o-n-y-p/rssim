from typing import final

from view.scheduler_view import SchedulerView
from database import FREIGHT_MAP


@final
class FreightMapSchedulerView(SchedulerView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
