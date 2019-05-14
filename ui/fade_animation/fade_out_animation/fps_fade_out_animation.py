from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class FPSFadeOutAnimation(FadeOutAnimation):
    """
    Implements fade-out animation for FPS view.
    """
    def __init__(self, fps_controller):
        """
        :param fps_controller:                  FPS controller
        """
        super().__init__(animation_object=fps_controller,
                         logger=getLogger('root.app.fps.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
