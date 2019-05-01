from view.scheduler_view import SchedulerView


class PassengerMapSchedulerView(SchedulerView):
    """
    Implements Scheduler view for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
