from logging import getLogger

from controller import *
from model.signal_model import SignalModel
from view.signal_view import SignalView
from ui.fade_animation.fade_in_animation.signal_fade_in_animation import SignalFadeInAnimation
from ui.fade_animation.fade_out_animation.signal_fade_out_animation import SignalFadeOutAnimation


class SignalController(MapBaseController):
    def __init__(self, model: SignalModel, view: SignalView, map_id, parent_controller, track, base_route):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.controller'))
        self.track = track
        self.base_route = base_route
        self.map_id = map_id
        self.view = view
        self.model = model
        self.fade_in_animation = SignalFadeInAnimation(self.view)
        self.fade_out_animation = SignalFadeOutAnimation(self.view)
        self.view.on_init_content()

    def create_signal_elements(self, track, base_route):
        pass

    @final
    def on_switch_to_green(self):
        self.model.on_switch_to_green()

    @final
    def on_switch_to_red(self):
        self.model.on_switch_to_red()
