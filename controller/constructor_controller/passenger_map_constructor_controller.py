from logging import getLogger

from controller.constructor_controller import ConstructorController


class PassengerMapConstructorController(ConstructorController):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller,
                         logger=getLogger('root.app.game.map.0.constructor.controller'))
