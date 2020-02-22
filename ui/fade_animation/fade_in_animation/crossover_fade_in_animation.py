from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class CrossoverFadeInAnimation(FadeInAnimation):
    def __init__(self, crossover_view):
        super().__init__(animation_object=crossover_view,
                         logger=getLogger(
                             f'root.app.game.map.{crossover_view.map_id}.crossover.{crossover_view.track_param_1}.{crossover_view.track_param_2}.{crossover_view.crossover_type}.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
