from typing import final

from controller.signal_controller import SignalController
from model.signal_model.passenger_map_signal_model import PassengerMapSignalModel
from view.signal_view.passenger_map_signal_view import PassengerMapSignalView


@final
class PassengerMapSignalController(SignalController):
    def __init__(self, map_controller, track, base_route):
        super().__init__(*self.create_signal_elements(track, base_route), map_id=0, parent_controller=map_controller,
                         track=track, base_route=base_route)

    def create_signal_elements(self, track, base_route):
        view = PassengerMapSignalView(controller=self, track=track, base_route=base_route)
        model = PassengerMapSignalModel(controller=self, view=view, track=track, base_route=base_route)
        return model, view
