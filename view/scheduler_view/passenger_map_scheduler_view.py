from view.scheduler_view import SchedulerView


class PassengerMapSchedulerView(SchedulerView):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
