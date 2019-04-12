from model.scheduler_model import SchedulerModel


class PassengerMapSchedulerModel(SchedulerModel):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
