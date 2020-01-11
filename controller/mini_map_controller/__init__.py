from logging import getLogger


from controller import *
from model.mini_map_model import MiniMapModel
from view.mini_map_view import MiniMapView
from ui.fade_animation.fade_in_animation.mini_map_fade_in_animation import MiniMapFadeInAnimation
from ui.fade_animation.fade_out_animation.mini_map_fade_out_animation import MiniMapFadeOutAnimation


class MiniMapController(MapBaseController):
    def __init__(self, model: MiniMapModel, view: MiniMapView, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.mini_map.controller'))
        self.map_id = map_id
        self.fade_in_animation = MiniMapFadeInAnimation(self)
        self.fade_out_animation = MiniMapFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()

    def create_mini_map_elements(self):
        pass

    @final
    def on_unlock_track(self, track):
        self.view.on_unlock_track(track)

    @final
    def on_unlock_environment(self, tier):
        self.view.on_unlock_environment(tier)
