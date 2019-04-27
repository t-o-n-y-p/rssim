from controller.scheduler_controller import SchedulerController


class PassengerMapSchedulerController(SchedulerController):
    """
    Implements Scheduler controller for passenger map (map_id = 0).
    """
    def __init__(self, map_controller):
        super().__init__(map_id=0, parent_controller=map_controller)
