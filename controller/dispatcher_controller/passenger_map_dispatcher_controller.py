from typing import final

from controller.dispatcher_controller import DispatcherController
from model.dispatcher_model.passenger_map_dispatcher_model import PassengerMapDispatcherModel
from view.dispatcher_view.passenger_map_dispatcher_view import PassengerMapDispatcherView
from database import PASSENGER_MAP


@final
class PassengerMapDispatcherController(DispatcherController):
    def __init__(self, map_controller):
        super().__init__(map_id=PASSENGER_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = PassengerMapDispatcherView(controller=self)
        model = PassengerMapDispatcherModel(controller=self, view=view)
        return view, model
