from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class MiniMapFadeInAnimation(FadeInAnimation):
    def __init__(self, mini_map_view):
        super().__init__(
            animation_object=mini_map_view,
            logger=getLogger(f'root.app.game.map.{mini_map_view.map_id}.mini_map.fade_in_animation')
        )
