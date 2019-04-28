from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class TrainFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Train view.
    """
    def __init__(self, train_controller):
        """
        :param train_controller:                Train controller
        """
        super().__init__(animation_object=train_controller,
                         logger=getLogger(f'root.app.game.map.train.{train_controller.train_id}.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
