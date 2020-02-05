from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.scheduler_fade_in_animation import SchedulerFadeInAnimation
from ui.fade_animation.fade_out_animation.scheduler_fade_out_animation import SchedulerFadeOutAnimation


class SchedulerController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.scheduler.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = SchedulerFadeInAnimation(self.view)
        self.fade_out_animation = SchedulerFadeOutAnimation(self.view)

    @abstractmethod
    def create_view_and_model(self):
        pass

    @final
    def on_unlock_track(self, track):
        self.model.on_unlock_track(track)

    @final
    def on_unlock_environment(self, tier):
        self.model.on_unlock_environment(tier)

    @final
    def on_leave_entry(self, entry_id):
        self.model.on_leave_entry(entry_id)
