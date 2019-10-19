from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class LicenseFadeInAnimation(FadeInAnimation):
    def __init__(self, license_controller):
        super().__init__(animation_object=license_controller,
                         logger=getLogger('root.app.license.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
