from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class SchedulerFadeOutAnimation(FadeOutAnimation):
    def __init__(self, scheduler_controller):
        super().__init__(animation_object=scheduler_controller,
                         logger=getLogger('root.app.game.map.scheduler.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
