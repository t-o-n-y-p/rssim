from typing import final

from controller.scheduler_controller import SchedulerController
from model.scheduler_model.passenger_map_scheduler_model import PassengerMapSchedulerModel
from view.scheduler_view.passenger_map_scheduler_view import PassengerMapSchedulerView


@final
class PassengerMapSchedulerController(SchedulerController):
    def __init__(self, map_controller):
        super().__init__(*self.create_scheduler_elements(), map_id=0, parent_controller=map_controller)

    def create_scheduler_elements(self):
        view = PassengerMapSchedulerView(controller=self)
        model = PassengerMapSchedulerModel(controller=self, view=view)
        return model, view
