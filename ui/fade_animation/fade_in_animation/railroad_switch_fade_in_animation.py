from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class RailroadSwitchFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for Railroad switch view.
    """
    def __init__(self, switch_controller):
        """
        :param switch_controller:               RailroadSwitch controller
        """
        super().__init__(animation_object=switch_controller,
                         logger=getLogger(
                             f'root.app.game.map.{switch_controller.map_id}.railroad_switch.{switch_controller.track_param_1}.{switch_controller.track_param_2}.{switch_controller.switch_type}.fade_in_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
