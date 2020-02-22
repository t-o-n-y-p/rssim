from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class SchedulerFadeInAnimation(FadeInAnimation):
    def __init__(self, scheduler_view):
        super().__init__(animation_object=scheduler_view,
                         logger=getLogger(f'root.app.game.map.{scheduler_view.map_id}.scheduler.fade_in_animation'))
