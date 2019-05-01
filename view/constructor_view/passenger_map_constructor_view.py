from view.constructor_view import ConstructorView


class PassengerMapConstructorView(ConstructorView):
    """
    Implements Constructor view for passenger map (map_id = 0).
    """
    def __init__(self):
        super().__init__(map_id=0)
