from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class RailroadSwitchFadeOutAnimation(FadeOutAnimation):
    def __init__(self, switch_controller):
        super().__init__(animation_object=switch_controller,
                         logger=getLogger(
                             f'root.app.game.map.{switch_controller.map_id}.railroad_switch.{switch_controller.track_param_1}.{switch_controller.track_param_2}.{switch_controller.switch_type}.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
