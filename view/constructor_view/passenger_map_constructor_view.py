from typing import final

from view.constructor_view import ConstructorView
from database import PASSENGER_MAP


@final
class PassengerMapConstructorView(ConstructorView):
    def __init__(self, controller):
        super().__init__(controller, map_id=PASSENGER_MAP)
