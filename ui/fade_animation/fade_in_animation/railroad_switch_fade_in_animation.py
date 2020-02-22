from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class RailroadSwitchFadeInAnimation(FadeInAnimation):
    def __init__(self, switch_view):
        super().__init__(animation_object=switch_view,
                         logger=getLogger(
                             f'root.app.game.map.{switch_view.map_id}.railroad_switch.{switch_view.track_param_1}.{switch_view.track_param_2}.{switch_view.switch_type}.fade_in_animation'
                         ))
