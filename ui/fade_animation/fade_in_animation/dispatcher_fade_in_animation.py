from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class DispatcherFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Dispatcher view.
    """
    def __init__(self, dispatcher_controller):
        """
        :param dispatcher_controller:           Dispatcher controller
        """
        super().__init__(animation_object=dispatcher_controller,
                         logger=getLogger(
                             f'root.app.game.map.{dispatcher_controller.map_id}.dispatcher.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
