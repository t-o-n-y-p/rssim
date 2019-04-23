from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class TrainFadeOutAnimation(FadeOutAnimation):
    def __init__(self, train_controller):
        super().__init__(animation_object=train_controller,
                         logger=getLogger(f'root.app.game.map.train.{train_controller.train_id}.fade_out_animation'))
        self.train_id = train_controller.train_id

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
