from typing import final

from database import FREIGHT_MAP
from view.narrator_view import NarratorView


@final
class FreightMapNarratorView(NarratorView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
