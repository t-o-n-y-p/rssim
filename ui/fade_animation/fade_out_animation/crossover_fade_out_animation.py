from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class CrossoverFadeOutAnimation(FadeOutAnimation):
    def __init__(self, crossover_controller):
        super().__init__(animation_object=crossover_controller,
                         logger=getLogger(
                             f'root.app.game.map.{crossover_controller.map_id}.crossover.{crossover_controller.track_param_1}.{crossover_controller.track_param_2}.{crossover_controller.crossover_type}.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
