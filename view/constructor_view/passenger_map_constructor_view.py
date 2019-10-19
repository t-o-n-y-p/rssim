from typing import final

from view.constructor_view import ConstructorView


@final
class PassengerMapConstructorView(ConstructorView):
    def __init__(self):
        super().__init__(map_id=0)
