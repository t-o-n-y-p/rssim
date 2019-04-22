from logging import getLogger

from ui.fade_animation.fade_in_animation import *


class LicenseFadeInAnimation(FadeInAnimation):
    def __init__(self, license_controller):
        super().__init__(animation_object=license_controller,
                         logger=getLogger('root.app.license.fade_in_animation'))

    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
