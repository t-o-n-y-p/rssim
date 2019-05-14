from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class SettingsFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Settings view.
    """
    def __init__(self, settings_controller):
        """
        :param settings_controller:             Settings controller
        """
        super().__init__(animation_object=settings_controller,
                         logger=getLogger('root.app.settings.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()
