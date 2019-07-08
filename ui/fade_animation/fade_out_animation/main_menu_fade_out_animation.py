from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class MainMenuFadeOutAnimation(FadeOutAnimation):
    def __init__(self, main_menu_controller):
        super().__init__(animation_object=main_menu_controller,
                         logger=getLogger('root.app.main_menu.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
