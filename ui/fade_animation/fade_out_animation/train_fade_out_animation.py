from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class TrainFadeOutAnimation(FadeOutAnimation):
    def __init__(self, train_view):
        super().__init__(
            animation_object=train_view, logger=getLogger(
                f'root.app.game.map.{train_view.map_id}.train.{train_view.train_id}.fade_out_animation'
            )
        )
