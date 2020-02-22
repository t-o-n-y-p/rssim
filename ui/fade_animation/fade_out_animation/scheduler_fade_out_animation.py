from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class SchedulerFadeOutAnimation(FadeOutAnimation):
    def __init__(self, scheduler_view):
        super().__init__(animation_object=scheduler_view,
                         logger=getLogger(
                             f'root.app.game.map.{scheduler_view.map_id}.scheduler.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
