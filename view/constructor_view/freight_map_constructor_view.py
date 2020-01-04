from typing import final

from view.constructor_view import ConstructorView
from database import FREIGHT_MAP


@final
class FreightMapConstructorView(ConstructorView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
