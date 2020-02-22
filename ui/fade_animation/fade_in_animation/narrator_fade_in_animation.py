from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class NarratorFadeInAnimation(FadeInAnimation):
    def __init__(self, narrator_view):
        super().__init__(animation_object=narrator_view,
                         logger=getLogger(f'root.app.game.map.{narrator_view.map_id}.narrator.fade_in_animation'))
