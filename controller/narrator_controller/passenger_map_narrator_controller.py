from typing import final

from controller.narrator_controller import NarratorController
from database import PASSENGER_MAP
from model.narrator_model.passenger_map_narrator_model import PassengerMapNarratorModel
from view.narrator_view.passenger_map_narrator_view import PassengerMapNarratorView


@final
class PassengerMapNarratorController(NarratorController):
    def __init__(self, map_controller):
        super().__init__(map_id=PASSENGER_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = PassengerMapNarratorView(controller=self)
        model = PassengerMapNarratorModel(controller=self, view=view)
        return view, model
