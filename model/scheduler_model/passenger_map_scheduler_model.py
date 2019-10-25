from model.scheduler_model import SchedulerModel


class PassengerMapSchedulerModel(SchedulerModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=0)
