from controller.scheduler_controller import SchedulerController


class PassengerMapSchedulerController(SchedulerController):
    def __init__(self, map_controller):
        super().__init__(map_id=0, parent_controller=map_controller)
