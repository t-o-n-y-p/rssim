from model.scheduler_model import SchedulerModel


class PassengerMapSchedulerModel(SchedulerModel):
    """
    Implements Scheduler model for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
