from logging import getLogger

from controller.scheduler_controller import SchedulerController


class PassengerMapSchedulerController(SchedulerController):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller,
                         logger=getLogger('root.app.game.map.0.scheduler.controller'))
