from typing import final

from controller.dispatcher_controller import DispatcherController
from model.dispatcher_model.passenger_map_dispatcher_model import PassengerMapDispatcherModel
from view.dispatcher_view.passenger_map_dispatcher_view import PassengerMapDispatcherView


@final
class PassengerMapDispatcherController(DispatcherController):
    def __init__(self, map_controller):
        super().__init__(*self.create_dispatcher_elements(), map_id=0, parent_controller=map_controller)

    def create_dispatcher_elements(self):
        view = PassengerMapDispatcherView(controller=self)
        model = PassengerMapDispatcherModel(controller=self, view=view)
        return model, view
