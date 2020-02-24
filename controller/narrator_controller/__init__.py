from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.narrator_fade_in_animation import NarratorFadeInAnimation
from ui.fade_animation.fade_out_animation.narrator_fade_out_animation import NarratorFadeOutAnimation


class NarratorController(MapBaseController, ABC):
    def __init__(self, map_id, parent_controller):
        super().__init__(map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.narrator.controller'))
        self.view, self.model = self.create_view_and_model()
        self.fade_in_animation = NarratorFadeInAnimation(self.view)
        self.fade_out_animation = NarratorFadeOutAnimation(self.view)
