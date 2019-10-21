from logging import getLogger

from controller import *


class SchedulerController(GameBaseController):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.scheduler.controller'))
        self.map_id = map_id

    @final
    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.parent_controller.on_close_schedule()

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)

    @final
    def on_unlock_environment(self, tier):
        self.model.on_unlock_environment(tier)

    @final
    def on_leave_entry(self, entry_id):
        self.model.on_leave_entry(entry_id)
