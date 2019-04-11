from logging import getLogger

from controller.railroad_switch_controller import RailroadSwitchController


class PassengerMapRailroadSwitchController(RailroadSwitchController):
    def __init__(self, map_controller, track_param_1, track_param_2, switch_type):
        super().__init__(
            parent_controller=map_controller, track_param_1=track_param_1, track_param_2=track_param_2,
            switch_type=switch_type,
            logger=getLogger(
                f'root.app.game.map.0.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.controller'
            )
        )
