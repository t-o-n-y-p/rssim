from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.crossover_fade_in_animation import CrossoverFadeInAnimation
from ui.fade_animation.fade_out_animation.crossover_fade_out_animation import CrossoverFadeOutAnimation


class CrossoverController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(
            map_id, parent_controller,
            logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.controller'
            )
        )
        self.view, self.model = self.create_view_and_model(track_param_1, track_param_2, crossover_type)
        self.track_param_1, self.track_param_2, self.crossover_type = track_param_1, track_param_2, crossover_type
        self.fade_in_animation = CrossoverFadeInAnimation(self.view)
        self.fade_out_animation = CrossoverFadeOutAnimation(self.view)

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self, positions):
        self.model.on_force_busy_off(positions)
