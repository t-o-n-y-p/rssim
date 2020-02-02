from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class SettingsFadeInAnimation(FadeInAnimation):
    def __init__(self, settings_view):
        super().__init__(animation_object=settings_view, logger=getLogger('root.app.settings.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
