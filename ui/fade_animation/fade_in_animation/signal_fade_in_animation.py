from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class SignalFadeInAnimation(FadeInAnimation):
    def __init__(self, signal_view):
        super().__init__(
            animation_object=signal_view, logger=getLogger(
                f'root.app.game.map.{signal_view.map_id}.signal.{signal_view.track}.{signal_view.base_route}.fade_in_animation'
            )
        )
