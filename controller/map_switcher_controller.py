from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.map_switcher_fade_in_animation import MapSwitcherFadeInAnimation
from ui.fade_animation.fade_out_animation.map_switcher_fade_out_animation import MapSwitcherFadeOutAnimation
from model.map_switcher_model import MapSwitcherModel
from view.map_switcher_view import MapSwitcherView


@final
class MapSwitcherController(GameBaseController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller,
                         logger=getLogger(f'root.app.game.map_switcher.controller'))
        self.view = MapSwitcherView(controller=self)
        self.model = MapSwitcherModel(controller=self, view=self.view)
        self.fade_in_animation = MapSwitcherFadeInAnimation(self.view)
        self.fade_out_animation = MapSwitcherFadeOutAnimation(self.view)

    def on_switch_map(self, new_map_id):
        self.model.on_switch_map(new_map_id)

    def on_unlock_map(self, map_id):
        self.view.on_unlock_map(map_id)

    def get_current_map_id(self):
        return self.model.currently_selected_map
