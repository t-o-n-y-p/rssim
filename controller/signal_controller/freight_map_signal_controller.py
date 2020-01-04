from typing import final

from controller.signal_controller import SignalController
from model.signal_model.freight_map_signal_model import FreightMapSignalModel
from view.signal_view.freight_map_signal_view import FreightMapSignalView
from database import FREIGHT_MAP


@final
class FreightMapSignalController(SignalController):
    def __init__(self, map_controller, track, base_route):
        super().__init__(*self.create_signal_elements(track, base_route), map_id=FREIGHT_MAP,
                         parent_controller=map_controller, track=track, base_route=base_route)

    def create_signal_elements(self, track, base_route):
        view = FreightMapSignalView(controller=self, track=track, base_route=base_route)
        model = FreightMapSignalModel(controller=self, view=view, track=track, base_route=base_route)
        return model, view
