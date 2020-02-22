from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class TrainRouteFadeInAnimation(FadeInAnimation):
    def __init__(self, train_route_view):
        super().__init__(animation_object=train_route_view,
                         logger=getLogger(
                             f'root.app.game.map.{train_route_view.map_id}.train_route.{train_route_view.track}.{train_route_view.train_route}.fade_in_animation'
                         ))
