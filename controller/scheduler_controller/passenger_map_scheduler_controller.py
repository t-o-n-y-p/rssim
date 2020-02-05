from typing import final

from controller.scheduler_controller import SchedulerController
from model.scheduler_model.passenger_map_scheduler_model import PassengerMapSchedulerModel
from view.scheduler_view.passenger_map_scheduler_view import PassengerMapSchedulerView
from database import PASSENGER_MAP


@final
class PassengerMapSchedulerController(SchedulerController):
    def __init__(self, map_controller):
        super().__init__(map_id=PASSENGER_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = PassengerMapSchedulerView(controller=self)
        model = PassengerMapSchedulerModel(controller=self, view=view)
        return view, model
