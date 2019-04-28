from ui.fade_animation import *


class FadeOutAnimation(FadeAnimation):
    """
    Base class for fade-out animations.
    """
    def __init__(self, animation_object, logger):
        """
        :param animation_object:                target object controller
        :param logger:                          telemetry instance
        """
        super().__init__(animation_object=animation_object, logger=logger)
        self.opacity_chart = [255, 238, 221, 204, 187, 170, 153, 136, 119, 102, 85, 68, 51, 34, 17, 0]

    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        pass

    @fade_animation_is_active
    def on_deactivate(self):
        """
        Deactivates the animation and notifies the listener about it.
        """
        self.is_activated = False
        if self.on_deactivate_listener is not None:
            self.on_deactivate_listener.on_fade_out_animation_deactivate()
