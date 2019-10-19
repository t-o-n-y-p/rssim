from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class SettingsFadeOutAnimation(FadeOutAnimation):
    def __init__(self, settings_controller):
        super().__init__(animation_object=settings_controller,
                         logger=getLogger('root.app.settings.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
