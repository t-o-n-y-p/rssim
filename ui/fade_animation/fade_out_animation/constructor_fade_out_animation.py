from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class ConstructorFadeOutAnimation(FadeOutAnimation):
    def __init__(self, constructor_controller):
        super().__init__(animation_object=constructor_controller,
                         logger=getLogger(
                             f'root.app.game.map.{constructor_controller.map_id}.constructor.fade_out_animation'
                         ))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
