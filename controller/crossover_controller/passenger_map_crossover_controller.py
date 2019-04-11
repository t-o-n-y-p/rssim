from logging import getLogger

from controller.crossover_controller import CrossoverController


class PassengerMapCrossoverController(CrossoverController):
    def __init__(self, map_controller, track_param_1, track_param_2, crossover_type):
        super()\
            .__init__(parent_controller=map_controller, track_param_1=track_param_1, track_param_2=track_param_2,
                      crossover_type=crossover_type,
                      logger=getLogger(
                          f'root.app.game.map.0.crossover.{track_param_1}.{track_param_2}.{crossover_type}.controller'
                      ))
