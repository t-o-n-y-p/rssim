from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.map_switcher_fade_in_animation import MapSwitcherFadeInAnimation
from ui.fade_animation.fade_out_animation.map_switcher_fade_out_animation import MapSwitcherFadeOutAnimation
from model.map_switcher_model import MapSwitcherModel
from view.map_switcher_view import MapSwitcherView


class MapSwitcherController(GameBaseController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller,
                         logger=getLogger(f'root.app.game.map_switcher.controller'))
        self.fade_in_animation = MapSwitcherFadeInAnimation(self)
        self.fade_out_animation = MapSwitcherFadeOutAnimation(self)
        self.view = MapSwitcherView(controller=self)
        self.model = MapSwitcherModel(controller=self, view=self.view)
        self.view.on_init_content()

    @final
    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.parent_controller.on_close_map_switcher()
