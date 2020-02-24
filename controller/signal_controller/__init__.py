from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.signal_fade_in_animation import SignalFadeInAnimation
from ui.fade_animation.fade_out_animation.signal_fade_out_animation import SignalFadeOutAnimation


class SignalController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller, track, base_route):
        super().__init__(map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.controller'))
        self.view, self.model = self.create_view_and_model(track, base_route)
        self.track, self.base_route = track, base_route
        self.fade_in_animation = SignalFadeInAnimation(self.view)
        self.fade_out_animation = SignalFadeOutAnimation(self.view)

    @final
    def on_switch_to_green(self):
        self.model.on_switch_to_green()

    @final
    def on_switch_to_red(self):
        self.model.on_switch_to_red()
