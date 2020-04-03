from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class CrossoverFadeOutAnimation(FadeOutAnimation):
    def __init__(self, crossover_view):
        super().__init__(
            animation_object=crossover_view, logger=getLogger(
                f'root.app.game.map.{crossover_view.map_id}.crossover.{crossover_view.track_param_1}.{crossover_view.track_param_2}.{crossover_view.crossover_type}.fade_out_animation'
            )
        )
