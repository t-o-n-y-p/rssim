from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class TrainRouteFadeOutAnimation(FadeOutAnimation):
    def __init__(self, train_route_controller):
        super().__init__(animation_object=train_route_controller,
                         logger=getLogger(
                             f'root.app.game.map.{train_route_controller.map_id}.train_route.{train_route_controller.track}.{train_route_controller.train_route}.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
