from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class DispatcherFadeOutAnimation(FadeOutAnimation):
    def __init__(self, dispatcher_view):
        super().__init__(
            animation_object=dispatcher_view, logger=getLogger(
                f'root.app.game.map.{dispatcher_view.map_id}.dispatcher.fade_out_animation'
            )
        )
