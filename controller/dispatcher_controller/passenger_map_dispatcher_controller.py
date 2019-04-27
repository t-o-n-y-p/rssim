from controller.dispatcher_controller import DispatcherController


class PassengerMapDispatcherController(DispatcherController):
    """
    Implements Dispatcher controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller):
        super().__init__(map_id=0, parent_controller=map_controller)
