from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class RailroadSwitchFadeOutAnimation(FadeOutAnimation):
    def __init__(self, switch_controller):
        super().__init__(animation_object=switch_controller,
                         logger=getLogger('root.app.game.map.railroad_switch.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
