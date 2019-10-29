from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.map_switcher_fade_in_animation import MapSwitcherFadeInAnimation
from ui.fade_animation.fade_out_animation.map_switcher_fade_out_animation import MapSwitcherFadeOutAnimation


class MapSwitcherController(GameBaseController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller,
                         logger=getLogger(f'root.app.game.map_switcher.controller'))
        self.fade_in_animation = MapSwitcherFadeInAnimation(self)
        self.fade_out_animation = MapSwitcherFadeOutAnimation(self)
        self.view = MapSwitcherView(controller=self)
        self.model = MapSwitcherModel(controller=self, view=self.view)
        self.view.on_init_content()
