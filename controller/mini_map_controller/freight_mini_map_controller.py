from typing import final


from controller.mini_map_controller import MiniMapController
from model.mini_map_model.freight_mini_map_model import FreightMiniMapModel
from view.mini_map_view.freight_mini_map_view import FreightMiniMapView
from database import FREIGHT_MAP


@final
class FreightMiniMapController(MiniMapController):
    def __init__(self, map_controller):
        super().__init__(map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_view_and_model(self):
        view = FreightMiniMapView(controller=self)
        model = FreightMiniMapModel(controller=self, view=view)
        return view, model
