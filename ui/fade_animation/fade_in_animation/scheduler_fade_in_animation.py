from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class SchedulerFadeInAnimation(FadeInAnimation):
    def __init__(self, scheduler_controller):
        super().__init__(animation_object=scheduler_controller,
                         logger=getLogger(
                             f'root.app.game.map.{scheduler_controller.map_id}.scheduler.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
