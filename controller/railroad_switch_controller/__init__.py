from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.railroad_switch_fade_in_animation import RailroadSwitchFadeInAnimation
from ui.fade_animation.fade_out_animation.railroad_switch_fade_out_animation import RailroadSwitchFadeOutAnimation


class RailroadSwitchController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, track_param_1, track_param_2, switch_type):
        logger_name \
            = f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.controller'
        super().__init__(map_id, parent_controller, logger=getLogger(logger_name))
        self.view, self.model = self.create_view_and_model(track_param_1, track_param_2, switch_type)
        self.track_param_1, self.track_param_2, self.switch_type = track_param_1, track_param_2, switch_type
        self.fade_in_animation = RailroadSwitchFadeInAnimation(self.view)
        self.fade_out_animation = RailroadSwitchFadeOutAnimation(self.view)

    @abstractmethod
    def create_view_and_model(self, track_param_1, track_param_2, switch_type):
        pass

    @final
    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    @final
    def on_force_busy_off(self):
        self.model.on_force_busy_off()
