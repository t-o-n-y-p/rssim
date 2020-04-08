from abc import ABC
from logging import getLogger
from typing import final

from controller import MapBaseController
from ui.fade_animation.fade_in_animation.railroad_switch_fade_in_animation import RailroadSwitchFadeInAnimation
from ui.fade_animation.fade_out_animation.railroad_switch_fade_out_animation import RailroadSwitchFadeOutAnimation


class RailroadSwitchController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, switch_type):
        super().__init__(
            map_id, parent_controller,
            logger=getLogger(
                f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.controller'
            )
        )
        self.view, self.model = self.create_view_and_model(track_param_1, track_param_2, switch_type)
        self.track_param_1, self.track_param_2, self.switch_type = track_param_1, track_param_2, switch_type
        self.fade_in_animation = RailroadSwitchFadeInAnimation(self.view)
        self.fade_out_animation = RailroadSwitchFadeOutAnimation(self.view)

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self):
        self.model.on_force_busy_off()
