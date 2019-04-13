from view.constructor_view import ConstructorView


class PassengerMapConstructorView(ConstructorView):
    def __init__(self):
        super().__init__()

    def on_update_map_id(self):
        self.map_id = 0
