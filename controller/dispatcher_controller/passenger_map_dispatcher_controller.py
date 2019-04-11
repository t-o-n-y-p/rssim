from logging import getLogger

from controller.dispatcher_controller import DispatcherController


class PassengerMapDispatcherController(DispatcherController):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller,
                         logger=getLogger('root.app.game.map.0.dispatcher.controller'))
