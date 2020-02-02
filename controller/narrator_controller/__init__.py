from logging import getLogger

from controller import *
from model.narrator_model import NarratorModel
from ui.fade_animation.fade_in_animation.narrator_fade_in_animation import NarratorFadeInAnimation
from ui.fade_animation.fade_out_animation.narrator_fade_out_animation import NarratorFadeOutAnimation
from view.narrator_view import NarratorView


class NarratorController(MapBaseController):
    def __init__(self, model: NarratorModel, view: NarratorView, map_id, parent_controller):
        super().__init__(model, view, map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.narrator.controller'))
        self.fade_in_animation = NarratorFadeInAnimation(self.view)
        self.fade_out_animation = NarratorFadeOutAnimation(self.view)

    def create_narrator_elements(self):
        pass
