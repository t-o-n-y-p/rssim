from logging import getLogger


from controller import *
from ui.fade_animation.fade_in_animation.mini_map_fade_in_animation import MiniMapFadeInAnimation
from ui.fade_animation.fade_out_animation.mini_map_fade_out_animation import MiniMapFadeOutAnimation


class MiniMapController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.mini_map.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = MiniMapFadeInAnimation(self.view)
        self.fade_out_animation = MiniMapFadeOutAnimation(self.view)

    @abstractmethod
    def create_view_and_model(self):
        pass

    @final
    def on_unlock_track(self, track):
        self.view.on_unlock_track(track)

    @final
    def on_unlock_environment(self, tier):
        self.view.on_unlock_environment(tier)
