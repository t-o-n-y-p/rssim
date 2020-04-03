from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class NarratorFadeOutAnimation(FadeOutAnimation):
    def __init__(self, narrator_view):
        super().__init__(
            animation_object=narrator_view,
            logger=getLogger(f'root.app.game.map.{narrator_view.map_id}.mini_map.fade_out_animation')
        )
