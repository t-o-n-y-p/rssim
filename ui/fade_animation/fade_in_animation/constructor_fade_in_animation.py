from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class ConstructorFadeInAnimation(FadeInAnimation):
    def __init__(self, constructor_view):
        super().__init__(animation_object=constructor_view,
                         logger=getLogger(
                             f'root.app.game.map.{constructor_view.map_id}.constructor.fade_in_animation'
                         ))
