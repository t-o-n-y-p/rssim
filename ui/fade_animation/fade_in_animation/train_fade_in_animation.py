from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class TrainFadeInAnimation(FadeInAnimation):
    def __init__(self, train_controller):
        super().__init__(animation_object=train_controller,
                         logger=getLogger(
                             f'root.app.game.map.{train_controller.map_id}.train.{train_controller.train_id}.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()
