from logging import getLogger

from controller import *
from model.scheduler_model import SchedulerModel
from view.scheduler_view import SchedulerView
from ui.fade_animation.fade_in_animation.scheduler_fade_in_animation import SchedulerFadeInAnimation
from ui.fade_animation.fade_out_animation.scheduler_fade_out_animation import SchedulerFadeOutAnimation


class SchedulerController(GameBaseController):
    def __init__(self, model: SchedulerModel, view: SchedulerView, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.scheduler.controller'))
        self.map_id = map_id
        self.fade_in_animation = SchedulerFadeInAnimation(self)
        self.fade_out_animation = SchedulerFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()

    def create_scheduler_elements(self):
        pass

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
