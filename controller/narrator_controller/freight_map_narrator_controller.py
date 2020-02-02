from typing import final

from controller.narrator_controller import NarratorController
from database import FREIGHT_MAP
from model.narrator_model.freight_map_narrator_model import FreightMapNarratorModel
from view.narrator_view.freight_map_narrator_view import FreightMapNarratorView


@final
class FreightMapNarratorController(NarratorController):
    def __init__(self, map_controller):
        super().__init__(*self.create_narrator_elements(), map_id=FREIGHT_MAP, parent_controller=map_controller)

    def create_narrator_elements(self):
        view = FreightMapNarratorView(controller=self)
        model = FreightMapNarratorModel(controller=self, view=view)
        return model, view
