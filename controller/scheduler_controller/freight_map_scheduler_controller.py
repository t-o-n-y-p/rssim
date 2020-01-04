from typing import final

from controller.scheduler_controller import SchedulerController
from model.scheduler_model.freight_map_scheduler_model import FreightMapSchedulerModel
from view.scheduler_view.freight_map_scheduler_view import FreightMapSchedulerView
from database import FREIGHT_MAP


@final
class FreightMapSchedulerController(SchedulerController):
    def __init__(self, map_controller):
        super().__init__(*self.create_scheduler_elements(), map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_scheduler_elements(self):
        view = FreightMapSchedulerView(controller=self)
        model = FreightMapSchedulerModel(controller=self, view=view)
        return model, view
