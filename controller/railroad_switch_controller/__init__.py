from logging import getLogger

from controller import *


class RailroadSwitchController(MapBaseController):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, switch_type):
        logger_name \
            = f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.controller'
        super().__init__(parent_controller=parent_controller, logger=getLogger(logger_name))
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.switch_type = switch_type
        self.map_id = map_id

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self):
        self.model.on_force_busy_off()
