from typing import final


from controller.mini_map_controller import MiniMapController
from model.mini_map_model.passenger_mini_map_model import PassengerMiniMapModel
from view.mini_map_view.passenger_mini_map_view import PassengerMiniMapView
from database import PASSENGER_MAP


@final
class PassengerMiniMapController(MiniMapController):
    def __init__(self, map_controller):
        super().__init__(*self.create_mini_map_elements(), map_id=PASSENGER_MAP, parent_controller=map_controller)

    def create_mini_map_elements(self):
        view = PassengerMiniMapView(controller=self)
        model = PassengerMiniMapModel(controller=self, view=view)
        return model, view
