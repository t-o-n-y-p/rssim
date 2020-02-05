from typing import final

from controller.dispatcher_controller import DispatcherController
from model.dispatcher_model.freight_map_dispatcher_model import FreightMapDispatcherModel
from view.dispatcher_view.freight_map_dispatcher_view import FreightMapDispatcherView
from database import FREIGHT_MAP


@final
class FreightMapDispatcherController(DispatcherController):
    def __init__(self, map_controller):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = FreightMapDispatcherView(controller=self)
        model = FreightMapDispatcherModel(controller=self, view=view)
        return view, model
