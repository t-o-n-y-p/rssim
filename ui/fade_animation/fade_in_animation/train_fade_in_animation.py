from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class TrainFadeInAnimation(FadeInAnimation):
    def __init__(self, train_controller):
        super().__init__(animation_object=train_controller,
                         logger=getLogger(
                             f'root.app.game.map.{train_controller.map_id}.train.{train_controller.train_id}.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
