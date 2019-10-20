from logging import getLogger

from controller import *


class CrossoverController(AppBaseController, GameBaseController, MapBaseController):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, crossover_type):
        super().__init__(
            parent_controller=parent_controller,
            logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.controller'
            )
        )
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.crossover_type = crossover_type
        self.map_id = map_id

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self, positions):
        self.model.on_force_busy_off(positions)
