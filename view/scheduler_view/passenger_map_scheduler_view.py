from view.scheduler_view import SchedulerView
from view import FRAMES_IN_ONE_HOUR


class PassengerMapSchedulerView(SchedulerView):
    def __init__(self):
        super().__init__(map_id=0)
        self.arrival_time_threshold = FRAMES_IN_ONE_HOUR
