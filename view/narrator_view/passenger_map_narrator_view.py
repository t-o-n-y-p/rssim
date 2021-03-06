from typing import final

from database import PASSENGER_MAP
from view.narrator_view import NarratorView


@final
class PassengerMapNarratorView(NarratorView):
    def __init__(self, controller):
        super().__init__(controller, map_id=PASSENGER_MAP)
