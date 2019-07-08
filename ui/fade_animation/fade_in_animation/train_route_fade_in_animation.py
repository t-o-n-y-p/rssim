from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class TrainRouteFadeInAnimation(FadeInAnimation):
    def __init__(self, train_route_controller):
        super().__init__(animation_object=train_route_controller,
                         logger=getLogger(
                             f'root.app.game.map.{train_route_controller.map_id}.train_route.{train_route_controller.track}.{train_route_controller.train_route}.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()
