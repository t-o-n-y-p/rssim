from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class TrainFadeOutAnimation(FadeOutAnimation):
    def __init__(self, train_controller):
        super().__init__(animation_object=train_controller,
                         logger=getLogger(
                             f'root.app.game.map.{train_controller.map_id}.train.{train_controller.train_id}.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
